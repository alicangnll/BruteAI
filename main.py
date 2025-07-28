# -*- coding: utf-8 -*-
"""
AI-Powered Wordlist Generator – Cross-Platform Version
Model: deepseek-ai/deepseek-coder-6.7b-instruct

• Resolved 'undefined symbol' error using SDPA instead of flash-attn.
• Added 8-bit quantization to reduce CUDA out of memory errors in Colab.
• Automatic model selection based on system capabilities added.
• Text is processed in chunks to reduce RAM usage.
• Prompts for multiple languages added.
• Advanced crawler integrated using Playwright to bypass protections.
• Environment cleanup function added.
• Cross-platform (Windows/macOS/Linux) compatibility ensured.
• Platform detection and indication of relevant installation steps added.
• Added additional filtering based on extracted text content.
• Added text cleaning step to improve AI output quality.
• Model generation parameter warnings resolved.
• Option to specify a custom model from HuggingFace via command-line argument added.
• Switched web crawling library from Selenium to Playwright.
• Added system dependency installation for Playwright on Linux/Colab.
• Further updated Playwright system dependencies based on error feedback and common requirements.
"""

import requests, logging, io
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
# Removed Selenium/WebDriver imports
# import undetected_chromedriver as uc
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import WebDriverException, TimeoutException
# from webdriver_manager.chrome import ChromeDriverManager

import fitz # PyMuPDF
import docx # python-docx
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig # Import BitsAndBytesConfig from transformers
from langdetect import detect
import torch
import os
import time # Import the time module
import gc # Import garbage collector
import platform # Import platform to check OS
import re # Import regex for word count
import sys # Import sys to access command line arguments
import argparse # Import argparse for cleaner argument parsing

# Add Playwright imports
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError


# Colab specific imports for clearing output (optional for this kind of cleanup)
# from IPython.display import clear_output
# --- Installation Information and Conditional Setup (For Colab or Local Use) ---

print(f"Operating System Detected: {platform.system()}")

# -------------------- SETTINGS --------------------
# MODEL_NAME = "google/gemma-2b-it" # Changed model to a smaller instruction-tuned model

# Model list - used when no custom model is specified or fails to load
# Order from largest to smallest
DEFAULT_MODEL_LIST = [
    "deepseek-ai/deepseek-coder-6.7b-instruct",  # Larger model
    "deepseek-ai/deepseek-coder-1.3b-instruct",  # Smaller model
    # "google/gemma-2b-it", # Removed gated model
    # Other model names can be added here if needed
]


SUPPORTED_LANGUAGES = {
    "en": "English", "fr": "French", "de": "German",
    "es": "Spanish", "pt": "Portuguese", "ru": "Russian", "tr": "Turkish"
}

# Updated SYSTEM_PROMPT to encourage broader extraction based on context
SYSTEM_PROMPT = "You are a specialized text analysis tool focused on finding potential login credentials. Your task is to identify and list potential usernames and passwords that are explicitly mentioned or can be reasonably inferred from the context of the provided text. You MUST adhere strictly to the requested output format. Provide the response ONLY as two distinct lists, one for usernames and one for passwords, each item prefixed by a hyphen. Include NO other text, explanations, introductions, conclusions, or conversational elements whatsoever. List all potential usernames and passwords found or inferred from the text."

# Updated TRANSLATED_PROMPTS to reflect the broader task
TRANSLATED_PROMPTS = {
    "en": "Analyze the following text and extract all potential usernames and passwords that are mentioned or can be inferred from the context. Output MUST be ONLY in this format:\n\nusername:\n- user1\n- user2\n...\n\npassword:\n- pass1\n- pass2\n...\n\nText to analyze:\n{body}\n\nResponse:",
    "tr": "Aşağıdaki metni incele ve metinde geçen veya bağlamdan çıkarılabilecek tüm muhtemel kullanıcı adı ve parola kelimelerini ayıkla. Çıktı SADECE şu formatta OLMALIDIR:\n\nusername:\n- kullanici1\n- kullanici2\n...\n\npassword:\n- parola1\n- parola1\n...\n\nAnaliz edilecek metin:\n{body}\n\nYanıt:",
    "es": "Analiza el siguiente texto y extrae todos los posibles nombres de usuario y contraseñas que se mencionan o se pueden inferir del contexto. La salida DEBE estar SOLAMENTE en este formato:\n\nusername:\n- usuario1\n- usuario2\n...\n\npassword:\n- contraseña1\n- contraseña2\n...\n\nTexto a analizar:\n{body}\n\nRespuesta:",
    "pt": "Analise o texto a seguir e extraia todos os possíveis nomes de usuário e senhas que são mencionados ou podem ser inferidos do contexto. A saída DEVE estar SOMENTE neste formato:\n\nusername:\n- usuario1\n- usuario2\n...\n\npassword:\n- senha1\n- senha2\n...\n\nTexto para analisar:\n{body}\n\nRespuesta:",
    "ru": "Проанализируйте следующий текст и извлеките все потенциальные имена пользователей и пароли, которые упоминаются или могут быть выведены из контекста. Вывод ДОЛЖЕН быть ТОЛЬКО в этом формате:\n\nusername:\n- пользователь1\n- пользователь2\n...\n\npassword:\n- пароль1\n- пароль2\n...\n\nТекст для анализа:\n{body}\n\nОтвет:",
    "de": "Analysieren Sie den folgenden Text und extrahieren Sie alle potenziellen Benutzernamen und Passwörter, die erwähnt werden oder aus dem Kontext abgeleitet werden können. Die Ausgabe MUSS NUR in diesem Format erfolgen:\n\nusername:\n- benutzername1\n- benutzername2\n...\n\npassword:\n- passwort1\n- passwort2\n...\n\nZu analysierender Text:\n{body}\n\nAntwort:",

}
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# -------------------- TEXT EXTRACTION --------------------
def extract_text_from_pdf(content_bytes):
    try:
        with fitz.open(stream=content_bytes, filetype="pdf") as doc:
            return "".join(p.get_text() for p in doc)
    except Exception as e:
        print(f"PDF Error: {e}") # Translated print statement
        return ""

def extract_text_from_docx(content_bytes):
    try:
        return "\n".join(p.text for p in docx.Document(io.BytesIO(content_bytes)).paragraphs)
    except Exception as e:
        print(f"DOCX Error: {e}") # Translated print statement
        return ""

# --- Text Cleaning Function ---
def clean_text(text):
    """Cleans text by removing extra whitespace, special characters, etc."""
    # Remove common unwanted characters (adjust as needed)
    cleaned = re.sub(r'[\r\n]+', '\n', text) # Normalize newlines
    cleaned = re.sub(r'[ \t]+', ' ', cleaned) # Normalize spaces
    cleaned = cleaned.strip()
    # Optional: Remove non-printable characters, careful not to remove potential password chars
    # import string
    # cleaned = ''.join(filter(lambda x: x in string.printable, cleaned))
    return cleaned


# -------------------- CRAWLER (Playwright) --------------------
# Rewritten crawl_website_advanced function using Playwright
def crawl_website_advanced(start_url, max_pages=None, requests_per_second=None, sleep_between_requests=None):
    print(f"\nStarting Playwright Crawler: {start_url} (limit: {max_pages or '∞'})") # Translated print statement

    text_contents = [] # List to store text of each page

    # Use sync_playwright for synchronous operations
    # Added context manager for p to ensure it's closed
    with sync_playwright() as p:
        # Launch Chromium browser (can choose 'firefox' or 'webkit' as well)
        # Use headless=True for running without a GUI
        browser = p.chromium.launch(headless=True)
        print("Browser launched successfully.") # Translated print statement

        visited, queue, count = set(), [start_url], 0
        start_domain = urlparse(start_url).netloc

        request_count = 0
        start_time = time.time()

        while queue:
            if max_pages and count >= max_pages: break

            # Rate limiting logic
            if requests_per_second is not None:
                elapsed_time = time.time() - start_time
                if elapsed_time < 1.0 and request_count >= requests_per_second:
                    time.sleep(1.0 - elapsed_time)
                    start_time = time.time()
                    request_count = 0
                elif elapsed_time >= 1.0:
                    start_time = time.time()
                    request_count = 0

            # Optional sleep between requests
            if sleep_between_requests is not None:
                time.sleep(sleep_between_requests)

            url = queue.pop(0)
            if url in visited: continue

            # --- Preliminary HEAD request to check content type ---
            # Keep the HEAD request check as it's faster than launching a browser page
            try:
                # Use a short timeout for the HEAD request
                # Use a common user agent
                head_response = requests.head(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'})
                head_response.raise_for_status()
                ctype = head_response.headers.get('content-type', '').lower()

                # Check if the content type is HTML or XML (sitemap)
                # Also explicitly skip known image/video/audio/application types
                if not (ctype.startswith('text/html') or ctype.startswith('application/xml')) or ctype.startswith(('image/', 'video/', 'audio/', 'application/')):
                     print(f"  Skipping non-HTML/XML or known binary content type (HEAD check): {url} ({ctype})") # Translated print statement
                     visited.add(url)
                     continue # Skip this URL if not HTML/XML or is a known binary type

            except requests.RequestException as e:
                 # HEAD request failed, maybe the server doesn't support HEAD, try GET with Playwright anyway?
                 # Or maybe the URL is just bad. Let's skip for now to be safe.
                 print(f"  ⚠️ HEAD request error, skipping: {url} ({e})"); # Translated print statement
                 visited.add(url)
                 continue # Skip if HEAD request fails
            # --- End of HEAD request check ---

            page = None # Initialize page variable
            try:
                # Create a new page/tab in the browser
                page = browser.new_page()
                print(f"[{count+1}] Loading: {url}") # Translated print statement

                # Navigate to the URL and wait for the network to be idle (or load state)
                # Use a longer timeout for page navigation
                page.goto(url, wait_until="networkidle", timeout=60000) # Increased timeout to 60 seconds
                request_count += 1 # Increment request count after a successful attempt

                # Check for common Cloudflare indicators or specific text after loading
                page_source = page.content() # Get the page content (HTML)
                if "Just a moment..." in page.title() or "Pardon Our Interruption" in page_source or "Enable JavaScript and cookies to continue" in page_source or "DDoS protection by Cloudflare" in page_source:
                     print(f"  ⚠️ Blocking detected, skipping or additional waiting might be needed: {url}") # Translated print statement
                     # More complex waiting or resolution logic could be added here (Translated comment)
                     visited.add(url)
                     # page.close() # Close the page - Handled in finally block now
                     # continue # Skip this page or retry (Translated comment)


                # BeautifulSoup for text extraction
                soup = BeautifulSoup(page_source, 'html.parser')
                for s in soup(['script', 'style']): s.decompose()
                page_text = soup.get_text(separator=' ', strip=True)

                # --- Heuristic check based on extracted text content ---
                # Clean the text first before checking length and word count
                cleaned_page_text = clean_text(page_text)

                # Count words in the extracted text
                word_count = len(re.findall(r'\w+', cleaned_page_text))
                min_word_threshold = 50 # Arbitrary threshold, can be adjusted

                if word_count < min_word_threshold:
                    print(f"  ⚠️ Page text is very short ({word_count} words), likely not a content page. Skipping: {url}") # Translated print statement
                    # Note: Text from pages skipped here is NOT added to text_contents,
                    # effectively excluding it from AI analysis. (Translated comment)
                    visited.add(urlparse(url)._replace(fragment="").geturl()) # Add to visited even if skipped
                    # page.close() # Close the page - Handled in finally block now
                    # continue # Skip processing this page for text and links

                if len(cleaned_page_text) < 100: # Also check raw character length after cleaning
                     print(f"  ⚠️ Page text is very short ({len(cleaned_page_text)} characters), likely not a content page. Skipping: {url}") # Translated print statement
                     # Note: Text from pages skipped here is NOT added to text_contents,
                     # effectively excluding it from AI analysis. (Translated comment)
                     visited.add(urlparse(url)._replace(fragment="").geturl()) # Add to visited even if skipped
                    #  page.close() # Close the page - Handled in finally block now
                    #  continue # Skip processing this page for text and links - Handled in finally block now

                if cleaned_page_text: # Append the cleaned text if it passed checks
                     text_contents.append(cleaned_page_text)

                # Extract links and add to queue
                for a in soup.find_all('a', href=True):
                    href = a['href']
                    # Ignore links that are clearly not web pages (images, files, etc.) based on extension
                    if href.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.css', '.js', '.pdf', '.zip', '.rar', '.tar', '.gz', '.mp4', '.mp3', '.exe', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx')):
                        continue
                    if href.startswith(('#', 'mailto:', 'tel:')): continue
                    full = urljoin(start_url, href)
                    # Clean fragment identifiers for comparison
                    full_parsed = urlparse(full)
                    full_clean = full_parsed._replace(fragment="").geturl()

                    # Only add internal links to the queue if not already visited or in queue
                    # Also check against visited set using the cleaned URL
                    if (urlparse(full_clean).netloc == start_domain and full_clean not in visited and full_clean not in [item.geturl() for item in map(urlparse, queue)]):
                         queue.append(full) # Add original URL with fragment if any


            except PlaywrightTimeoutError as e:
                print(f"  ⚠️ Playwright timeout error: {url} ({e})"); # Translated print statement
                visited.add(url)
                # if page: page.close() # Ensure page is closed on error - Handled in finally
                # continue # Handled in finally
            except Exception as e:
                print(f"  ⚠️ General error during Playwright page processing: {url} ({e})"); # Translated print statement
                visited.add(url)
                # if page: page.close() # Ensure page is closed on error - Handled in finally
                # continue # Handled in finally
            finally:
                 if page and not page.is_closed():
                      page.close() # Close the page after processing
                 # Add to visited set even if an error occurred during page processing
                 # This prevents infinite loops on problematic pages
                 visited.add(urlparse(url)._replace(fragment="").geturl()); # Added this line here
                 count += 1 # Increment count even on error, if page attempt was made
                 print(f"  ✅ Attempted processing: {url}") # Changed to attempted processing


        # Browser will be closed automatically by the 'with' statement
        print("\nBrowser closed.") # Translated print statement


    return text_contents # Return list of text contents


# -------------------- AI ANALYSIS --------------------
tokenizer = None
model = None
device = None
torch_dtype = None # Declare torch_dtype globally
selected_model_name = None # Store the name of the successfully loaded model

def is_colab():
    # Check specifically for Colab environment variables
    return 'COLAB_GPU' in os.environ or 'COLAB_TPU_ADDR' in os.environ

def clean_environment():
    """Cleans up memory (GPU and variables). Suitable for Colab and local environments."""
    print("Cleaning up memory...") # Translated print statement
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        print("GPU memory cleared.") # Translated print statement

    # Delete large variables if they exist (Translated comment)
    global full_text, text_contents, all_users, all_passes
    # Check if the variable is in the global scope before trying to delete (Translated comment)
    # Use a list comprehension and then iterate to avoid modifying the list while iterating (Translated comment)
    vars_to_delete = [var_name for var_name in ['full_text', 'text_contents', 'all_users', 'all_passes'] if var_name in globals()]
    for var_name in vars_to_delete:
        try:
            del globals()[var_name]
            # print(f"'{var_name}' variable deleted.") # Optional: print deleted variables (Translated comment)
        except NameError:
            pass # Should not happen with the check above, but as a safeguard (Translated comment)

    gc.collect() # Run garbage collector (Translated comment)
    print("Memory cleanup complete.") # Translated print statement


# Modified load_model_and_tokenizer to accept a custom model name
def load_model_and_tokenizer(custom_model_name: str = None):
    global tokenizer, model, device, torch_dtype, selected_model_name
    if model is not None and tokenizer is not None:
        print(f"Model '{selected_model_name}' is already loaded.") # Translated print statement
        return True # Model is already loaded

    use_gpu = torch.cuda.is_available()
    device = "cuda" if use_gpu else "cpu"
    print(f"Device Used: {device.upper()}") # Translated print statement

    models_to_try = []
    if custom_model_name:
        print(f"Attempting custom model: '{custom_model_name}'") # Translated print statement
        models_to_try.append(custom_model_name)

    # Add default models if no custom model or if custom model failed
    # Only add default models if the custom model is not the same as the first default model
    if not custom_model_name or custom_model_name != DEFAULT_MODEL_LIST[0]:
         models_to_try.extend(DEFAULT_MODEL_LIST)
    elif custom_model_name == DEFAULT_MODEL_LIST[0] and len(DEFAULT_MODEL_LIST) > 1:
        # If custom model is the first default, still add the rest of the default list
        models_to_try.extend(DEFAULT_MODEL_LIST[1:])


    for model_name in models_to_try:
        # Avoid trying the same model name twice if it was explicitly added as custom
        if model_name == selected_model_name:
             continue

        print(f"\nStage: Loading model '{model_name}'...") # Translated print statement
        try:
            # Determine loading configuration based on device and environment (Translated comment)
            if use_gpu:
                # Try 8-bit quantization first if GPU is available (Translated comment)
                try:
                    print("⚡ Attempting 8-bit quantization...") # Translated print statement
                    # Note: bitsandbytes and accelerate are typically needed for quantization (Translated comment)
                    # Ensure these are installed (added to pip install list) (Translated comment)
                    bnb_config = BitsAndBytesConfig(
                        load_in_8bit=True,
                        bnb_4bit_quant_type="nf4", # Optional: can try "nf4" or "fp4" for 4-bit (Translated comment)
                        bnb_4bit_compute_dtype=torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float32,
                        bnb_4bit_use_double_quant=True,
                    )
                    model = AutoModelForCausalLM.from_pretrained(
                        model_name,
                        trust_remote_code=True,
                        quantization_config=bnb_config,
                        attn_implementation="sdpa" if use_gpu else "eager" # Use sdpa on GPU, eager on CPU (Translated comment)
                    )
                    torch_dtype = None # torch_dtype is managed by quantization (Translated comment)
                    print(f"✅ Model '{model_name}' loaded successfully with 8-bit quantization.") # Translated print statement

                except Exception as e:
                    print(f"⚠️ 8-bit quantization failed: {e}. Trying normal loading...") # Translated print statement
                    # Fallback to normal loading (float16/bfloat16 on GPU) (Translated comment)
                    if torch.cuda.is_bf16_supported():
                        torch_dtype = torch.bfloat16
                        print(f"⚡ bfloat16 support available. Data Type: {torch_dtype}") # Translated print statement
                    else:
                        torch_dtype = torch.float16
                        print(f"⚠️ bfloat16 not supported, using float16. Data Type: {torch_dtype}") # Translated print statement

                    # Clean up memory before trying normal loading (Translated comment)
                    clean_environment() # Use the more general cleanup function (Translated comment)

                    model = AutoModelForCausalLM.from_pretrained(
                        model_name,
                        trust_remote_code=True,
                        torch_dtype=torch_dtype,
                        attn_implementation="sdpa"
                    ).to(device)
                    print(f"✅ Normal loading ({'bfloat16' if torch_dtype == torch.bfloat16 else 'float16'}) with model '{model_name}' completed successfully.") # Translated print statement

            else: # Running on CPU (Translated comment)
                torch_dtype = torch.float32 # CPU typically uses float32 (Translated comment)
                print(f"⚠️ GPU not found. Device: CPU (Operations may be slower)") # Translated print statement
                model = AutoModelForCausalLM.from_pretrained(
                    model_name,
                    trust_remote_code=True,
                    torch_dtype=torch_dtype,
                    attn_implementation="eager" # Eager recommended for CPU (Translated comment)
                ).to(device)
                print(f"✅ Model '{model_name}' loaded successfully.") # Translated print statement


            # If model loading is successful, load tokenizer and break loop (Translated comment)
            tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
            print(f"Tokenizer '{model_name}' loaded successfully.") # Translated print statement
            selected_model_name = model_name # Store the name of the successfully loaded model (Translated comment)
            return True # Successfully loaded a model and tokenizer

        except Exception as e:
            print(f"⚠️ Failed to load model '{model_name}': {e}") # Translated print statement
            # Clean up in case of partial loading or errors before trying the next model (Translated comment)
            # Ensure model and tokenizer are set to None if loading failed (Translated comment)
            del model
            del tokenizer
            clean_environment() # Clean up memory aggressively (Translated comment)

            model, tokenizer, torch_dtype = None, None, None # Reset variables (Translated comment)

    print("\n❌ Error: None of the models in the list could be loaded. Please try a smaller model or use a runtime with more memory.") # Translated print statement
    selected_model_name = None
    return False # Failed to load any model


def detect_language(text: str) -> str:
    try: lang = detect(text); return lang if lang in SUPPORTED_LANGUAGES else "en"
    except: return "en"

def build_prompt(text: str, snippet_length: int = 15000) -> str:
    # Use the provided snippet_length, default to 15000 if not provided (Translated comment)
    # Now build_prompt takes a text chunk, snippet_length limits the size of the chunk used in the prompt (Translated comment)
    snippet = text[:snippet_length]
    lang = detect_language(snippet)
    # print(f"Detected language: {SUPPORTED_LANGUAGES.get(lang, 'Unknown')} ({lang})") # Reduced logging (Translated comment)
    user_prompt = TRANSLATED_PROMPTS.get(lang, TRANSLATED_PROMPTS["en"]).format(body=snippet)
    return f"SYSTEM: {SYSTEM_PROMPT}\nUSER: {user_prompt}\nASSISTANT:"


def generate_credentials(text: str, snippet_length: int = 15000, max_gen_tokens: int = 512) -> str:
    # Added snippet_length parameter to generate_credentials (Translated comment)
    global torch_dtype # Access global torch_dtype (Translated comment)
    if model is None or tokenizer is None:
        print("Model or tokenizer not loaded."); return "" # Translated print statement
    # Pass text chunk and snippet_length to build_prompt (Translated comment)
    prompt = build_prompt(text, snippet_length=snippet_length)
    try:
        # Autocasting for mixed precision in case float16 or bfloat16 is used, not needed with 8-bit (Translated comment)
        if getattr(model, "is_loaded_in_8bit", False) or getattr(model, "is_loaded_in_4bit", False):
             # If model is quantized, don't use autocast (Translated comment)
             inputs = tokenizer(prompt, return_tensors="pt").to(device)
             # Removed temperature=0.7 (Translated comment)
             outputs = model.generate(**inputs, max_new_tokens=max_gen_tokens, pad_token_id=tokenizer.eos_token_id)
        else:
            # Use autocast for float16/bfloat16 if on GPU (Translated comment)
            with torch.cuda.amp.autocast(enabled=device == 'cuda' and torch_dtype in [torch.float16, torch.bfloat16]):
                 inputs = tokenizer(prompt, return_tensors="pt").to(device)
                 # Removed temperature=0.7 (Translated comment)
                 outputs = model.generate(**inputs, max_new_tokens=max_gen_tokens, pad_token_id=tokenizer.eos_token_id)

        output_tokens = outputs[0][len(inputs.input_ids[0]):]
        generated_part = tokenizer.decode(output_tokens, skip_special_tokens=True)
        return generated_part.strip()
    except Exception as e:
        print(f"Text generation error: {e}"); return "" # Translated print statement

def parse_output(out: str):
    usernames, passwords, current = [], [], None
    # Process output line by line to find and extract lists (Translated comment)
    lines = out.splitlines()
    process_lines = False # Flag to indicate if we are within the list section (Translated comment)

    for line in lines:
        l = line.strip()
        lower_l = l.lower()

        # Start processing lines after encountering "username:" or "password:" (Translated comment)
        if lower_l.startswith("username:"):
            current = "u"
            process_lines = True
            continue # Move to the next line after header (Translated comment)

        if lower_l.startswith("password:"):
            current = "p"
            process_lines = True
            continue # Move to the next line after header (Translated comment)

        # If we are processing lines and encounter a blank line or new section, stop (Translated comment)
        # Added more potential stopping indicators based on AI conversational output (Translated comment)
        if process_lines and (not l or lower_l.startswith(("text to analyze:", "response:", "sistem:", "user:", "assistant:", "analiz edilecek metin:", "yanıt:"))):
             # This is a heuristic to stop processing if the model includes extra sections (Translated comment)
             process_lines = False
             current = None
             # Don't break immediately, allow parsing to potentially find another section later, though less likely with strict prompt (Translated comment)

        if process_lines:
            # Check if the line starts with a list marker (- , •, *) and strip it (Translated comment)
            # Be slightly more permissive in parsing to capture more potential entries (Translated comment)
            if l.startswith(("-", "•", "*")): # Still prefer list markers (Translated comment)
                 item = l.lstrip("-•* ").strip()
                 if item: usernames.append(item) if current == "u" else passwords.append(item)
            # Removed the logic to try and parse lines without list markers - keeping some structure is important (Translated comment)


    return usernames, passwords

def save_wordlist(words, filename):
    # Limit to top 50 unique words - Keeping this limit for file size, but AI might output more (Translated comment)
    # The user wants at least 50 output, let's adjust the saving logic to save all found unique words, (Translated comment)
    # not limited to 50, to meet the user's quantity expectation better, while still keeping them unique. (Translated comment)
    unique_words = sorted(list(set(words)))
    if not unique_words: print(f"No words found for {filename}."); return # Translated print statement
    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(unique_words))
    print(f"{len(unique_words)} words written to {filename}.") # Translated print statement


# -------------------- MAIN EXECUTION FUNCTION --------------------
# Modified run_wordlist_generator to accept custom_model_name
def run_wordlist_generator(target_site: str, max_pages: int = None, requests_per_second=None, sleep_between_requests=None, snippet_length: int = 15000, max_gen_tokens: int = 512, custom_model_name: str = None):
    # Define output filenames based on the target site domain (Translated comment)
    domain = urlparse(target_site).netloc.replace("www.", "")
    user_file = f"{domain}_username_wordlist.txt"
    pass_file = f"{domain}_password_wordlist.txt"

    # Delete existing wordlist files if they exist (Translated comment)
    if os.path.exists(user_file):
        os.remove(user_file)
        print(f"Existing file deleted: {user_file}") # Translated print statement
    if os.path.exists(pass_file):
        os.remove(pass_file)
        print(f"Existing file deleted: {pass_file}") # Translated print statement

    print("Stage: Loading model and tokenizer...") # Translated print statement
    # Pass the custom_model_name to the load function (Translated comment)
    if not load_model_and_tokenizer(custom_model_name=custom_model_name):
      print("Model could not be loaded, stopping process.") # Translated print statement
      return


    print("Stage: Crawling website and collecting text...") # Translated print statement
    # Use the advanced crawler which returns a list of page texts (Translated comment)
    text_contents = crawl_website_advanced(target_site, max_pages=max_pages, requests_per_second=requests_per_second, sleep_between_requests=sleep_between_requests)

    # Clean up memory after crawling (This function is now more general cleanup) (Translated comment)
    clean_environment() # Use the more general cleanup function (Translated comment)

    if not text_contents: # Check if the list is empty (Translated comment)
        print("No text could be extracted from the website. Stopping process."); return # Translated print statement

    all_users, all_passes = [], [] # Lists to aggregate results from each chunk (Translated comment)

    print(f"Stage: AI model generating text ({len(text_contents)} chunks)...") # Translated print statement
    # Iterate through each text chunk (which is a page text in this case) and generate credentials (Translated comment)
    for i, text_chunk in enumerate(text_contents):
        # Skip empty chunks (Translated comment)
        if not text_chunk.strip():
            print(f"  Chunk {i+1}/{len(text_contents)} is empty, skipping.") # Translated print statement
            continue

        print(f"  Processing chunk {i+1}/{len(text_contents)}...") # Translated print statement
        # Pass the text_chunk and snippet_length to generate_credentials (Translated comment)
        # Use snippet_length here to control how much of each page is sent to the model (Translated comment)
        raw_output = generate_credentials(text_chunk, snippet_length=snippet_length, max_gen_tokens=max_gen_tokens) # Pass snippet_length
        if not raw_output:
            print(f"  No AI response received for chunk {i+1}. Skipping."); continue # Translated print statement

        # Removed the print of raw_output to keep console output clean (Translated comment)
        # print(f"  Chunk {i+1} AI response:\n{raw_output}")
        users, passes = parse_output(raw_output)
        all_users.extend(users) # Aggregate users (Translated comment)
        all_passes.extend(passes) # Aggregate passes (Translated comment)

    # Clean up memory after AI processing (Translated comment)
    clean_environment() # Use the more general cleanup function (Translated comment)

    print("Stage: Parsing output and creating wordlists...") # Translated print statement
    # The parsing and aggregation is already done in the loop (Translated comment)
    # No need to parse raw_output again here (Translated comment)

    print(f"Total potential usernames found (including duplicates): {len(all_users)}") # Translated print statement
    print(f"Total potential passwords found (including duplicates): {len(all_passes)}") # Translated print statement


    print("Stage: Saving wordlists to files...") # Translated print statement
    # Save the aggregated and unique wordlists (Translated comment)
    save_wordlist(all_users, user_file)
    save_wordlist(all_passes, pass_file)

    print(f"Process complete. Wordlists saved to '{user_file}' and '{pass_file}' files.") # Translated print statement
    # Add instructions for finding files locally (Translated comment)
    print("You can find these files in the directory where the script is being run.") # Translated print statement


# --- Command Line Argument Handling ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI-Powered Wordlist Generator") # Translated help message
    parser.add_argument("target_site", help="Starting URL of the website to crawl") # Translated help message
    parser.add_argument("--max_pages", type=int, default=None, help="Maximum number of pages to crawl") # Translated help message
    parser.add_argument("--requests_per_second", type=float, default=None, help="Maximum requests per second (rate limiting)") # Translated help message
    parser.add_argument("--sleep_between_requests", type=float, default=None, help="Time to wait between requests (in seconds)") # Translated help message
    parser.add_argument("--snippet_length", type=int, default=15000, help="Maximum length of text snippets sent to AI") # Translated help message
    parser.add_argument("--max_gen_tokens", type=int, default=512, help="Maximum number of tokens the AI model will generate") # Translated help message
    parser.add_argument("--custom_model_name", type=str, default=None, help="Custom model name from HuggingFace (e.g., 'meta-llama/Llama-2-7b-hf')") # Translated help message

    # In a Colab notebook, sys.argv is ['/path/to/ipykernel_launcher.py', ...] (Translated comment)
    # When running as a script, it's ['your_script_name.py', ...] (Translated comment)
    # We need to handle Colab's specific sys.argv structure or use a workaround (Translated comment)
    # A common workaround in Colab is to manually provide args for testing (Translated comment)
    # Or, if running as a script, argparse works directly. (Translated comment)
    # Let's assume it's run as a script for argparse to work as intended. (Translated comment)
    # If running in Colab cell, the user might need to simulate sys.argv or call run_wordlist_generator directly. (Translated comment)

    # Check if running in Colab and provide instructions (Translated comment)
    if 'google.colab' in sys.modules:
        print("\nColab environment detected. Command line arguments may not work directly.") # Translated print statement
        print("You can call the run_wordlist_generator function directly to set parameters.") # Translated print statement
        print("Example: run_wordlist_generator('https://targetsite.com', max_pages=10, custom_model_name='deepseek-ai/deepseek-coder-1.3b-instruct')") # Translated print statement
        # In Colab, you might need to manually set args for testing argparse (Translated comment)
        # Example (uncomment and modify to test): (Translated comment)
        # sys.argv = ['ipykernel_launcher.py', 'https://alicangonullu.com', '--max_pages', '5', '--custom_model_name', 'deepseek-ai/deepseek-coder-1.3b-instruct'] (Translated comment)
        # try: (Translated comment)
        #     args = parser.parse_args() (Translated comment)
        #     print(f"\nArguments Parsed: {args}") (Translated comment)
        #     # Call the main function with parsed arguments (Translated comment)
        #     run_wordlist_generator( (Translated comment)
        #         target_site=args.target_site, (Translated comment)
        #         max_pages=args.max_pages, (Translated comment)
        #         requests_per_second=args.requests_per_second, (Translated comment)
        #         sleep_between_requests=args.sleep_between_requests, (Translated comment)
        #         snippet_length=args.snippet_length, (Translated comment)
        #         max_gen_tokens=args.max_gen_tokens, (Translated comment)
        #         custom_model_name=args.custom_model_name (Translated comment)
        #     ) (Translated comment)
        # except SystemExit: (Translated comment)
        #     # argparse.parse_args() calls sys.exit() on error/help, catch it in Colab (Translated comment)
        #     pass (Translated comment)

    else:
        # Standard script execution outside of Colab (Translated comment)
        args = parser.parse_args()
        print(f"\nArguments Parsed: {args}") # Translated print statement
        # Call the main function with parsed arguments (Translated comment)
        run_wordlist_generator(
            target_site=args.target_site,
            max_pages=args.max_pages,
            requests_per_second=args.requests_per_second,
            sleep_between_requests=args.sleep_between_requests,
            snippet_length=args.snippet_length,
            max_gen_tokens=args.max_gen_tokens,
            custom_model_name=args.custom_model_name
        )