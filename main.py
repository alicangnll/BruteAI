# -*- coding: utf-8 -*-
"""
AI-Powered Wordlist Generator – Cross-Platform Version
Model: deepseek-ai/deepseek-coder-6.7b-instruct

This script crawls a website, collects its text content, and uses an AI model
to generate potential username and password lists.
"""

import os
import gc
import io
import re
import time
import platform
import argparse
import requests
import docx
import fitz  # PyMuPDF
import torch
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from langdetect import detect
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
import undetected_chromedriver as uc
from selenium.common.exceptions import WebDriverException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

# -------------------- SETTINGS --------------------

MODEL_LIST = [
    "deepseek-ai/deepseek-coder-6.7b-instruct",  # Large model
    "deepseek-ai/deepseek-coder-1.3b-instruct",  # Small model
]

SUPPORTED_LANGUAGES = {
    "en": "English", "fr": "French", "de": "German",
    "es": "Spanish", "pt": "Portuguese", "ru": "Russian", "tr": "Turkish"
}

SYSTEM_PROMPT = (
    "You are a specialized text analysis tool focused on finding potential "
    "login credentials. Your task is to identify and list potential usernames "
    "and passwords that are explicitly mentioned or can be reasonably inferred "
    "from the context of the provided text. You MUST adhere strictly to the "
    "requested output format. Provide the response ONLY as two distinct lists, "
    "one for usernames and one for passwords, each item prefixed by a hyphen. "
    "Include NO other text, explanations, introductions, conclusions, or "
    "conversational elements whatsoever. List all potential usernames and "
    "passwords found or inferred from the text."
)

# This dictionary is a feature for multilingual support and remains as is.
TRANSLATED_PROMPTS = {
    "en": (
        "Analyze the following text and extract all potential usernames and "
        "passwords that are mentioned or can be inferred from the context. "
        "Output MUST be ONLY in this format:\n\n"
        "username:\n- user1\n- user2\n...\n\n"
        "password:\n- pass1\n- pass2\n...\n\n"
        "Text to analyze:\n{body}\n\nResponse:"
    ),
    "tr": (
        "Aşağıdaki metni incele ve metinde geçen veya bağlamdan çıkarılabilecek "
        "tüm muhtemel kullanıcı adı ve parola kelimelerini ayıkla. Çıktı SADECE "
        "şu formatta OLMALIDIR:\n\n"
        "username:\n- kullanici1\n- kullanici2\n...\n\n"
        "password:\n- parola1\n- parola1\n...\n\n"
        "Analiz edilecek metin:\n{body}\n\nYanıt:"
    ),
}


# -------------------- HELPER FUNCTIONS --------------------

def extract_text_from_pdf(content_bytes):
    try:
        with fitz.open(stream=content_bytes, filetype="pdf") as doc:
            return "".join(p.get_text() for p in doc)
    except Exception as e:
        print(f"PDF error: {e}")
        return ""

def extract_text_from_docx(content_bytes):
    try:
        doc = docx.Document(io.BytesIO(content_bytes))
        return "\n".join(p.text for p in doc.paragraphs)
    except Exception as e:
        print(f"DOCX error: {e}")
        return ""

def clean_text(text):
    """Cleans text by removing extra whitespace and special characters."""
    cleaned = re.sub(r'[\r\n]+', '\n', text)
    cleaned = re.sub(r'[ \t]+', ' ', cleaned)
    return cleaned.strip()


# -------------------- CRAWLER --------------------

def crawl_website_advanced(start_url, max_pages=50):
    print(f"\nStarting Advanced Crawler: {start_url} (limit: {max_pages or '∞'})")
    driver_path = None
    try:
        driver_path = ChromeDriverManager().install()
        print(f"ChromeDriver downloaded/found: {driver_path}")
    except Exception as e:
        print(f"⚠️ Could not download ChromeDriver: {e}")
        print("Please ensure Google Chrome is installed on your system.")
        return []

    options = uc.ChromeOptions()
    options.add_argument('--headless')
    if platform.system() == "Linux":
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36')

    driver = None
    text_contents = []
    try:
        driver = uc.Chrome(options=options, driver_executable_path=driver_path)
        print("Browser started successfully.")
        visited, queue, count = set(), [start_url], 0
        start_domain = urlparse(start_url).netloc

        while queue and (not max_pages or count < max_pages):
            url = queue.pop(0)
            if url in visited:
                continue

            try:
                print(f"[{count + 1}/{max_pages or '∞'}] Loading: {url}")
                driver.get(url)
                WebDriverWait(driver, 45).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

                if "Just a moment..." in driver.title or "DDoS protection by Cloudflare" in driver.page_source:
                    print(f"  ⚠️ Protection detected, skipping: {url}")
                    visited.add(url)
                    continue

                page_source = driver.page_source
                soup = BeautifulSoup(page_source, 'html.parser')
                for s in soup(['script', 'style']):
                    s.decompose()
                
                page_text = clean_text(soup.get_text(separator=' ', strip=True))
                word_count = len(re.findall(r'\w+', page_text))

                if word_count < 50:
                    print(f"  ⚠️ Page text too short ({word_count} words), skipping.")
                else:
                    text_contents.append(page_text)
                    print(f"  ✅ Successfully processed and text added.")

                visited.add(url)
                count += 1

                for a in soup.find_all('a', href=True):
                    href = a['href']
                    if href.startswith(('#', 'mailto:', 'tel:')) or href.lower().endswith(('.pdf', '.zip', '.jpg', '.png')):
                        continue
                    
                    full_url = urljoin(start_url, href)
                    full_clean = urlparse(full_url)._replace(fragment="").geturl()

                    if urlparse(full_clean).netloc == start_domain and full_clean not in visited and full_clean not in queue:
                        queue.append(full_url)
            
            except (WebDriverException, TimeoutException) as e:
                print(f"  ⚠️ Browser error or timeout: {url} ({e})")
            except Exception as e:
                print(f"  ⚠️ General error: {url} ({e})")
            
            if url not in visited:
                visited.add(url)

    finally:
        if driver:
            driver.quit()
            print("\nBrowser closed.")
    return text_contents


# -------------------- AI ANALYSIS --------------------

tokenizer = None
model = None
device = None
selected_model_name = None

def clean_memory():
    """Cleans up memory (GPU and variables)."""
    print("Cleaning up memory...")
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        print("GPU memory cleared.")
    
    vars_to_delete = [var for var in ['full_text', 'text_contents', 'all_users', 'all_passes'] if var in globals()]
    for var_name in vars_to_delete:
        del globals()[var_name]

    gc.collect()
    print("Memory cleanup complete.")

def load_model_and_tokenizer():
    global tokenizer, model, device, selected_model_name
    if model and tokenizer:
        print(f"Model '{selected_model_name}' is already loaded.")
        return True

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using Device: {device.upper()}")

    for model_name in MODEL_LIST:
        print(f"\nStep: Loading model '{model_name}'...")
        try:
            bnb_config = None
            if device == "cuda":
                print("⚡ Attempting 8-bit quantization...")
                bnb_config = BitsAndBytesConfig(load_in_8bit=True)
            
            model_instance = AutoModelForCausalLM.from_pretrained(
                model_name,
                trust_remote_code=True,
                quantization_config=bnb_config,
                torch_dtype=torch.float16 if device == "cuda" else torch.float32,
                attn_implementation="sdpa" if device == "cuda" else "eager"
            )
            if not bnb_config:
                model_instance.to(device)
            
            model = model_instance
            tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
            selected_model_name = model_name
            print(f"✅ Model and Tokenizer '{model_name}' loaded successfully.")
            return True
        except Exception as e:
            print(f"⚠️ Could not load model '{model_name}': {e}")
            clean_memory()

    print("\n❌ Error: Failed to load any of the listed models.")
    return False

def detect_language(text: str) -> str:
    try:
        lang = detect(text)
        return lang if lang in SUPPORTED_LANGUAGES else "en"
    except Exception:
        return "en"

def build_prompt(text: str, snippet_length: int = 15000) -> str:
    snippet = text[:snippet_length]
    lang = detect_language(snippet)
    user_prompt = TRANSLATED_PROMPTS.get(lang, TRANSLATED_PROMPTS["en"])
    return f"SYSTEM: {SYSTEM_PROMPT}\nUSER: {user_prompt.format(body=snippet)}\nASSISTANT:"

def generate_credentials(text: str, snippet_length: int, max_gen_tokens: int) -> str:
    if not model or not tokenizer:
        print("Model or tokenizer not loaded.")
        return ""
    
    prompt = build_prompt(text, snippet_length)
    try:
        inputs = tokenizer(prompt, return_tensors="pt").to(device)
        with torch.no_grad():
            outputs = model.generate(
                **inputs, 
                max_new_tokens=max_gen_tokens, 
                pad_token_id=tokenizer.eos_token_id
            )
        output_tokens = outputs[0][len(inputs.input_ids[0]):]
        return tokenizer.decode(output_tokens, skip_special_tokens=True).strip()
    except Exception as e:
        print(f"Text generation error: {e}")
        return ""

def parse_output(out: str):
    usernames, passwords, current = [], [], None
    lines = out.splitlines()
    for line in lines:
        l = line.strip().lower()
        if l.startswith("username:"):
            current = "u"
            continue
        if l.startswith("password:"):
            current = "p"
            continue
        
        if current and l.startswith("-"):
            item = line.strip().lstrip("- ").strip()
            if item:
                if current == "u":
                    usernames.append(item)
                else:
                    passwords.append(item)
    return usernames, passwords

def save_wordlist(words, filename):
    unique_words = sorted(list(set(words)))[:50]
    if not unique_words:
        print(f"No words found for '{filename}'.")
        return
    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(unique_words))
    print(f"✅ {len(unique_words)} words written to '{filename}'.")


# -------------------- MAIN EXECUTION FUNCTION --------------------
def main(args):
    domain = urlparse(args.url).netloc.replace("www.", "")
    user_file = f"{domain}_username_wordlist.txt"
    pass_file = f"{domain}_password_wordlist.txt"

    for f in [user_file, pass_file]:
        if os.path.exists(f):
            os.remove(f)
            print(f"Deleted existing file: {f}")

    print("Step 1/4: Loading model and tokenizer...")
    if not load_model_and_tokenizer():
        return

    print("\nStep 2/4: Crawling website and collecting text...")
    text_contents = crawl_website_advanced(args.url, max_pages=args.max_pages)
    clean_memory()

    if not text_contents:
        print("Could not extract text from the website. Halting process.")
        return

    all_users, all_passes = [], []
    print(f"\nStep 3/4: Generating text with AI model (in {len(text_contents)} chunks)...")
    for i, chunk in enumerate(text_contents):
        if not chunk.strip():
            continue
        print(f"  Processing chunk {i + 1}/{len(text_contents)}...")
        raw_output = generate_credentials(chunk, args.snippet_length, args.max_gen_tokens)
        if raw_output:
            users, passes = parse_output(raw_output)
            all_users.extend(users)
            all_passes.extend(passes)
    clean_memory()

    print("\nStep 4/4: Saving wordlists to files...")
    print(f"Total potential usernames (unique): {len(set(all_users))}")
    print(f"Total potential passwords (unique): {len(set(all_passes))}")
    save_wordlist(all_users, user_file)
    save_wordlist(all_passes, pass_file)

    print(f"\nProcess complete. You can find the files in this directory: {os.getcwd()}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="AI-Powered Wordlist Generator.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("url", type=str, help="Target website URL to analyze (e.g., https://example.com)")
    parser.add_argument("--max-pages", type=int, default=50, help="Maximum number of pages to crawl (default: 50)")
    parser.add_argument("--snippet-length", type=int, default=15000, help="Length of the text snippet to send to the AI (default: 15000)")
    parser.add_argument("--max-gen-tokens", type=int, default=512, help="Maximum number of tokens for the AI to generate (default: 512)")
    
    args = parser.parse_args()
    main(args)