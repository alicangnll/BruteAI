# -*- coding: utf-8 -*-
"""
AI-Powered Wordlist Generator – Cross-Platform Version
Model: deepseek-ai/deepseek-coder-6.7b-instruct

• Resolved 'undefined symbol' error using SDPA instead of flash-attn.
• Added 8-bit quantization to reduce CUDA out of memory errors in Colab.
• Automatic model selection based on system capabilities added.
• Text is processed in chunks to reduce RAM usage.
• Prompts for multiple languages added, with a requirement for at least 50 usernames/passwords.
• Crawler updated from Selenium to Playwright for better stability and performance.
• Environment cleanup function added.
• Cross-platform (Windows/macOS/Linux) compatibility ensured.
• Platform detection and indication of relevant installation steps added.
• Added additional filtering based on extracted text content.
• Added text cleaning step to improve AI output quality.
• Model generation parameter warnings resolved.
• Option to specify a custom model from HuggingFace via command-line argument added.
"""

import requests
import logging
import io
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import fitz  # PyMuPDF
import docx  # python-docx
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from langdetect import detect
import torch
import os
import time
import gc
import platform
import re
import sys
import argparse

# --- Playwright Imports ---
# Playwright, Selenium'a göre daha modern ve stabil bir alternatiftir.
# Cloudflare gibi korumaları aşmada daha başarılı olabilir.
try:
    from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
except ImportError:
    print("Playwright kütüphanesi bulunamadı.")
    print("Lütfen 'pip install playwright' komutuyla yükleyin.")
    print("Ardından tarayıcıları kurmak için 'playwright install' komutunu çalıştırın.")
    sys.exit(1)


# --- Installation Information and Conditional Setup ---

print(f"Operating System Detected: {platform.system()}")
print("Bu araç, web sitelerini taramak için Playwright ve Chromium kullanır.")
print("Eğer 'playwright install' komutunu çalıştırmadıysanız, script ilk çalıştırmada tarayıcıyı otomatik olarak indirmeye çalışabilir.")
print("-" * 20)


# -------------------- SETTINGS --------------------
DEFAULT_MODEL_LIST = [
    "deepseek-ai/deepseek-coder-6.7b-instruct",
    "deepseek-ai/deepseek-coder-1.3b-instruct",
]

SUPPORTED_LANGUAGES = {
    "en": "English", "fr": "French", "de": "German",
    "es": "Spanish", "pt": "Portuguese", "ru": "Russian", "tr": "Turkish"
}

# Sisteme en az 50+50 kelime üretme zorunluluğu eklendi.
SYSTEM_PROMPT = "You are a specialized text analysis tool focused on finding potential login credentials. Your task is to identify and list potential usernames and passwords that are explicitly mentioned or can be reasonably inferred from the context of the provided text. You MUST generate at least 50 potential usernames and at least 50 potential passwords. If you cannot find enough from the text, generate relevant variations based on the context. You MUST adhere strictly to the requested output format. Provide the response ONLY as two distinct lists, one for usernames and one for passwords, each item prefixed by a hyphen. Include NO other text, explanations, introductions, conclusions, or conversational elements whatsoever."

# Çevrilmiş prompt'lara da 50+50 kuralı eklendi.
TRANSLATED_PROMPTS = {
    "en": "Analyze the following text and extract potential usernames and passwords. You MUST generate at least 50 usernames and at least 50 passwords. If you cannot find enough from the text, generate relevant variations based on the context. Output MUST be ONLY in this format:\n\nusername:\n- user1\n- user2\n...\n\npassword:\n- pass1\n- pass2\n...\n\nText to analyze:\n{body}\n\nResponse:",
    "tr": "Aşağıdaki metni incele ve potansiyel kullanıcı adları ile parolaları çıkar. En az 50 kullanıcı adı ve en az 50 parola üretmek ZORUNLUSUN. Metinden yeterli sayıda bulamazsan, bağlama göre ilgili varyasyonları üret. Çıktı SADECE şu formatta OLMALIDIR:\n\nusername:\n- kullanici1\n- kullanici2\n...\n\npassword:\n- parola1\n- parola2\n...\n\nAnaliz edilecek metin:\n{body}\n\nYanıt:",
    "es": "Analiza el siguiente texto y extrae posibles nombres de usuario y contraseñas. DEBES generar al menos 50 nombres de usuario y al menos 50 contraseñas. Si no puedes encontrar suficientes en el texto, genera variaciones relevantes basadas en el contexto. La salida DEBE estar SOLAMENTE en este formato:\n\nusername:\n- usuario1\n- usuario2\n...\n\npassword:\n- contraseña1\n- contraseña2\n...\n\nTexto a analizar:\n{body}\n\nRespuesta:",
    "pt": "Analise o texto a seguir e extraia possíveis nomes de usuário e senhas. Você DEVE gerar pelo menos 50 nomes de usuário e pelo menos 50 senhas. Se não conseguir encontrar o suficiente no texto, gere variações relevantes com base no contexto. A saída DEVE ser SOMENTE neste formato:\n\nusername:\n- usuario1\n- usuario2\n...\n\npassword:\n- senha1\n- senha2\n...\n\nTexto para analisar:\n{body}\n\nResposta:",
    "ru": "Проанализируйте следующий текст и извлеките потенциальные имена пользователей и пароли. Вы ДОЛЖНЫ сгенерировать не менее 50 имен пользователей и не менее 50 паролей. Если вы не можете найти достаточно из текста, сгенерируйте соответствующие варианты на основе контекста. Вывод ДОЛЖЕН быть ТОЛЬКО в этом формате:\n\nusername:\n- пользователь1\n- пользователь2\n...\n\npassword:\n- пароль1\n- пароль2\n...\n\nТекст для анализа:\n{body}\n\nОтвет:",
    "de": "Analysieren Sie den folgenden Text und extrahieren Sie potenzielle Benutzernamen und Passwörter. Sie MÜSSEN mindestens 50 Benutzernamen und mindestens 50 Passwörter generieren. Wenn Sie aus dem Text nicht genügend finden können, generieren Sie relevante Variationen basierend auf dem Kontext. Die Ausgabe MUSS NUR in diesem Format erfolgen:\n\nusername:\n- benutzername1\n- benutzername2\n...\n\npassword:\n- passwort1\n- passwort2\n...\n\nZu analysierender Text:\n{body}\n\nAntwort:",
}

# -------------------- TEXT EXTRACTION & CLEANING --------------------
def extract_text_from_pdf(content_bytes):
    try:
        with fitz.open(stream=content_bytes, filetype="pdf") as doc:
            return "".join(p.get_text() for p in doc)
    except Exception as e:
        print(f"PDF Hatası: {e}")
        return ""

def extract_text_from_docx(content_bytes):
    try:
        return "\n".join(p.text for p in docx.Document(io.BytesIO(content_bytes)).paragraphs)
    except Exception as e:
        print(f"DOCX Hatası: {e}")
        return ""

def clean_text(text):
    cleaned = re.sub(r'[\r\n]+', '\n', text)
    cleaned = re.sub(r'[ \t]+', ' ', cleaned)
    return cleaned.strip()


# -------------------- PLAYWRIGHT CRAWLER --------------------
def crawl_website_advanced(start_url, max_pages=None, requests_per_second=None, sleep_between_requests=None):
    print(f"\nPlaywright Crawler Başlatılıyor: {start_url} (limit: {max_pages or '∞'})")
    text_contents = []
    
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(headless=True)
        except Exception as e:
            print(f"HATA: Playwright tarayıcısı başlatılamadı: {e}")
            print("Lütfen 'playwright install' komutunu çalıştırarak gerekli tarayıcı dosyalarını kurduğunuzdan emin olun.")
            return []

        # Ortak bir kullanıcı aracısı (user-agent) belirleyelim
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
        )
        page = context.new_page()

        visited, queue, count = set(), [start_url], 0
        start_domain = urlparse(start_url).netloc

        request_count = 0
        start_time = time.time()

        while queue:
            if max_pages and count >= max_pages:
                break

            # Hız sınırlama mantığı
            if requests_per_second:
                elapsed_time = time.time() - start_time
                if elapsed_time < 1.0 and request_count >= requests_per_second:
                    time.sleep(1.0 - elapsed_time)
                    start_time = time.time()
                    request_count = 0
                elif elapsed_time >= 1.0:
                    start_time = time.time()
                    request_count = 0

            if sleep_between_requests:
                time.sleep(sleep_between_requests)

            url = queue.pop(0)
            if url in visited:
                continue

            try:
                print(f"[{count+1}] Yükleniyor: {url}")
                # Sayfaya git ve içeriğin yüklenmesini bekle
                page.goto(url, wait_until='domcontentloaded', timeout=45000)
                request_count += 1

                # Cloudflare gibi JS korumalarını kontrol et
                if "Just a moment..." in page.title() or "DDoS protection by Cloudflare" in page.content():
                    print(f"  ⚠️ JS Koruması algılandı, sayfa atlanıyor: {url}")
                    visited.add(url)
                    continue

                page_source = page.content()
                soup = BeautifulSoup(page_source, 'html.parser')
                for s in soup(['script', 'style']):
                    s.decompose()
                page_text = soup.get_text(separator=' ', strip=True)
                cleaned_page_text = clean_text(page_text)

                word_count = len(re.findall(r'\w+', cleaned_page_text))
                min_word_threshold = 50

                if word_count < min_word_threshold:
                    print(f"  ⚠️ Sayfa metni çok kısa ({word_count} kelime), içerik sayfası olmayabilir. Atlanıyor: {url}")
                    visited.add(urlparse(url)._replace(fragment="").geturl())
                    continue

                if cleaned_page_text:
                    text_contents.append(cleaned_page_text)

                # Linkleri çıkar ve sıraya ekle
                for a in soup.find_all('a', href=True):
                    href = a['href']
                    if href.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.css', '.js', '.pdf', '.zip', '.rar', '.exe')):
                        continue
                    if href.startswith(('#', 'mailto:', 'tel:')):
                        continue
                    
                    full = urljoin(start_url, href)
                    full_clean = urlparse(full)._replace(fragment="").geturl()

                    if urlparse(full_clean).netloc == start_domain and full_clean not in visited and full_clean not in queue:
                        queue.append(full_clean)

            except PlaywrightTimeoutError:
                print(f"  ⚠️ Tarayıcı zaman aşımı: {url}")
            except Exception as e:
                print(f"  ⚠️ Genel hata: {url} ({e})")
            
            finally:
                visited.add(urlparse(url)._replace(fragment="").geturl())
                count += 1
                if 'e' not in locals() or not e: # Eğer hata oluşmadıysa başarılı mesajı yazdır
                     print(f"  ✅ Başarıyla işlendi: {url}")


        browser.close()
        print("\nTarayıcı kapatıldı.")

    return text_contents


# -------------------- AI ANALYSIS --------------------
tokenizer = None
model = None
device = None
torch_dtype = None
selected_model_name = None

def clean_environment():
    print("Bellek temizleniyor...")
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        print("GPU belleği temizlendi.")
    
    vars_to_delete = [var_name for var_name in ['full_text', 'text_contents', 'all_users', 'all_passes'] if var_name in globals()]
    for var_name in vars_to_delete:
        try:
            del globals()[var_name]
        except NameError:
            pass
    
    gc.collect()
    print("Bellek temizleme tamamlandı.")

def load_model_and_tokenizer(custom_model_name: str = None):
    global tokenizer, model, device, torch_dtype, selected_model_name
    if model and tokenizer:
        print(f"Model '{selected_model_name}' zaten yüklü.")
        return True

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Kullanılan Cihaz: {device.upper()}")

    models_to_try = [custom_model_name] + DEFAULT_MODEL_LIST if custom_model_name else DEFAULT_MODEL_LIST

    for model_name in list(dict.fromkeys(models_to_try)): # Yinelenenleri kaldır
        print(f"\nAşama: '{model_name}' modeli yükleniyor...")
        try:
            if device == "cuda":
                try:
                    print("⚡ 8-bit niceleme deneniyor...")
                    bnb_config = BitsAndBytesConfig(
                        load_in_8bit=True,
                        bnb_4bit_quant_type="nf4",
                        bnb_4bit_compute_dtype=torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float32,
                        bnb_4bit_use_double_quant=True,
                    )
                    model = AutoModelForCausalLM.from_pretrained(
                        model_name, trust_remote_code=True, quantization_config=bnb_config, attn_implementation="sdpa"
                    )
                    torch_dtype = None
                    print(f"✅ Model '{model_name}' 8-bit niceleme ile başarıyla yüklendi.")
                except Exception as e:
                    print(f"⚠️ 8-bit niceleme başarısız: {e}. Normal yükleme deneniyor...")
                    torch_dtype = torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float16
                    clean_environment()
                    model = AutoModelForCausalLM.from_pretrained(
                        model_name, trust_remote_code=True, torch_dtype=torch_dtype, attn_implementation="sdpa"
                    ).to(device)
                    print(f"✅ Normal yükleme ({'bfloat16' if torch_dtype == torch.bfloat16 else 'float16'}) tamamlandı.")
            else:
                torch_dtype = torch.float32
                print("⚠️ GPU bulunamadı. CPU üzerinde çalışılıyor (işlemler yavaş olabilir).")
                model = AutoModelForCausalLM.from_pretrained(
                    model_name, trust_remote_code=True, torch_dtype=torch_dtype, attn_implementation="eager"
                ).to(device)
                print(f"✅ Model '{model_name}' başarıyla yüklendi.")

            tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
            selected_model_name = model_name
            return True

        except Exception as e:
            print(f"⚠️ '{model_name}' modeli yüklenemedi: {e}")
            clean_environment()
            model, tokenizer, torch_dtype = None, None, None

    print("\n❌ Hata: Listede bulunan modellerden hiçbiri yüklenemedi.")
    return False

def detect_language(text: str) -> str:
    try:
        lang = detect(text)
        return lang if lang in SUPPORTED_LANGUAGES else "en"
    except:
        return "en"

def build_prompt(text: str, snippet_length: int = 15000) -> str:
    snippet = text[:snippet_length]
    lang = detect_language(snippet)
    user_prompt = TRANSLATED_PROMPTS.get(lang, TRANSLATED_PROMPTS["en"]).format(body=snippet)
    return f"SYSTEM: {SYSTEM_PROMPT}\nUSER: {user_prompt}\nASSISTANT:"

def generate_credentials(text: str, snippet_length: int = 15000, max_gen_tokens: int = 1024) -> str:
    global torch_dtype
    if not model or not tokenizer:
        print("Model veya tokenizer yüklenmemiş.")
        return ""
    
    prompt = build_prompt(text, snippet_length=snippet_length)
    try:
        if getattr(model, "is_loaded_in_8bit", False):
            inputs = tokenizer(prompt, return_tensors="pt").to(device)
            outputs = model.generate(**inputs, max_new_tokens=max_gen_tokens, pad_token_id=tokenizer.eos_token_id)
        else:
            with torch.cuda.amp.autocast(enabled=(device == 'cuda' and torch_dtype in [torch.float16, torch.bfloat16])):
                inputs = tokenizer(prompt, return_tensors="pt").to(device)
                outputs = model.generate(**inputs, max_new_tokens=max_gen_tokens, pad_token_id=tokenizer.eos_token_id)

        output_tokens = outputs[0][len(inputs.input_ids[0]):]
        return tokenizer.decode(output_tokens, skip_special_tokens=True).strip()
    except Exception as e:
        print(f"Metin üretme hatası: {e}")
        return ""

def parse_output(out: str):
    usernames, passwords, current = [], [], None
    lines = out.splitlines()
    process_lines = False

    for line in lines:
        l = line.strip()
        lower_l = l.lower()

        if lower_l.startswith("username:"):
            current = "u"
            process_lines = True
            continue
        if lower_l.startswith("password:"):
            current = "p"
            process_lines = True
            continue
        
        if process_lines and (not l or lower_l.startswith(("text to analyze:", "response:"))):
            process_lines = False
            current = None

        if process_lines and l.startswith(("-", "•", "*")):
            item = l.lstrip("-•* ").strip()
            if item:
                (usernames if current == "u" else passwords).append(item)
    
    return usernames, passwords

def save_wordlist(words, filename):
    unique_words = sorted(list(set(words)))
    if not unique_words:
        print(f"'{filename}' için kelime bulunamadı.")
        return
    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(unique_words))
    print(f"{len(unique_words)} kelime '{filename}' dosyasına yazıldı.")


# -------------------- MAIN EXECUTION FUNCTION --------------------
def run_wordlist_generator(target_site: str, max_pages: int = None, requests_per_second=None, sleep_between_requests=None, snippet_length: int = 15000, max_gen_tokens: int = 1024, custom_model_name: str = None):
    domain = urlparse(target_site).netloc.replace("www.", "")
    user_file = f"{domain}_username_wordlist.txt"
    pass_file = f"{domain}_password_wordlist.txt"

    if os.path.exists(user_file): os.remove(user_file)
    if os.path.exists(pass_file): os.remove(pass_file)

    print("Aşama: Model ve tokenizer yükleniyor...")
    if not load_model_and_tokenizer(custom_model_name=custom_model_name):
        print("Model yüklenemedi, işlem durduruluyor.")
        return

    print("Aşama: Web sitesi taranıyor ve metin toplanıyor...")
    text_contents = crawl_website_advanced(target_site, max_pages=max_pages, requests_per_second=requests_per_second, sleep_between_requests=sleep_between_requests)
    
    clean_environment()

    if not text_contents:
        print("Web sitesinden metin çıkarılamadı. İşlem durduruluyor.")
        return

    all_users, all_passes = [], []
    print(f"Aşama: AI modeli metin üretiyor ({len(text_contents)} parça)...")
    for i, text_chunk in enumerate(text_contents):
        if not text_chunk.strip(): continue
        print(f"  Parça {i+1}/{len(text_contents)} işleniyor...")
        raw_output = generate_credentials(text_chunk, snippet_length=snippet_length, max_gen_tokens=max_gen_tokens)
        if not raw_output:
            print(f"  Parça {i+1} için AI yanıtı alınamadı. Atlanıyor.")
            continue
        users, passes = parse_output(raw_output)
        all_users.extend(users)
        all_passes.extend(passes)

    clean_environment()

    print("Aşama: Çıktı ayrıştırılıyor ve wordlist'ler oluşturuluyor...")
    print(f"Toplam potansiyel kullanıcı adı bulundu (tekrarlar dahil): {len(all_users)}")
    print(f"Toplam potansiyel parola bulundu (tekrarlar dahil): {len(all_passes)}")

    print("Aşama: Wordlist'ler dosyalara kaydediliyor...")
    save_wordlist(all_users, user_file)
    save_wordlist(all_passes, pass_file)

    print(f"\nİşlem tamamlandı. Wordlist'ler '{user_file}' ve '{pass_file}' dosyalarına kaydedildi.")
    print("Bu dosyaları script'in çalıştığı dizinde bulabilirsiniz.")


# --- Command Line Argument Handling ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI Destekli Wordlist Oluşturucu")
    parser.add_argument("target_site", help="Taranacak web sitesinin başlangıç URL'si")
    parser.add_argument("--max_pages", type=int, default=None, help="Taranacak maksimum sayfa sayısı")
    parser.add_argument("--requests_per_second", type=float, default=None, help="Saniye başına maksimum istek (hız sınırlama)")
    parser.add_argument("--sleep_between_requests", type=float, default=None, help="İstekler arası bekleme süresi (saniye)")
    parser.add_argument("--snippet_length", type=int, default=15000, help="AI'a gönderilecek metin parçacıklarının maksimum uzunluğu")
    parser.add_argument("--max_gen_tokens", type=int, default=1024, help="AI modelinin üreteceği maksimum token sayısı")
    parser.add_argument("--custom_model_name", type=str, default=None, help="HuggingFace'den özel model adı (örn: 'meta-llama/Llama-2-7b-hf')")

    if 'google.colab' in sys.modules:
        print("\nColab ortamı algılandı. Komut satırı argümanları doğrudan çalışmayabilir.")
        print("Parametreleri ayarlamak için run_wordlist_generator fonksiyonunu doğrudan çağırabilirsiniz.")
        print("Örnek: run_wordlist_generator('https://hedefsite.com', max_pages=10)")
    else:
        args = parser.parse_args()
        print(f"\nAyrıştırılan Argümanlar: {args}")
        run_wordlist_generator(
            target_site=args.target_site,
            max_pages=args.max_pages,
            requests_per_second=args.requests_per_second,
            sleep_between_requests=args.sleep_between_requests,
            snippet_length=args.snippet_length,
            max_gen_tokens=args.max_gen_tokens,
            custom_model_name=args.custom_model_name
        )
