# 🔐 BruteAI – AI-powered Wordlist Generator

## 🇬🇧 English – English Guide

**BruteAI** is an AI-powered tool that helps you generate targeted and effective wordlists from website content.

### 🚀 Features

  - AI-based content analysis
  - Advanced crawler that bypasses protections like Cloudflare
  - **Automatic language detection** for accurate analysis
  - Quantization to reduce CUDA memory errors
  - Cross-platform (Windows/macOS/Linux) compatibility
  - Automatic hardware detection and model selection
  - **Automatic file naming** (e.g., `example.com_username_wordlist.txt`)

### 🔧 Installation

To install the required Python libraries, run the following command in the project's root directory:

```bash
pip install -r requirements.txt
```

### 🛠️ Usage

You can run the tool from the terminal by providing the target site address directly.

```bash
python bruteai.py "https://example.com" --max-pages 10
```

**Parameters:**
| Parameter | Description | Type | Default |
| :--- | :--- | :--- | :--- |
| `url` | **(Required)** The full address of the website to crawl. | string | None |
| `--max-pages` | *(Optional)* Maximum number of pages to crawl. | integer | `50` |
| `--snippet-length` | *(Optional)* Length of the text snippet sent to the AI. | integer | `15000` |
| `--max-gen-tokens`| *(Optional)* Maximum number of tokens for the AI to generate. | integer | `512` |


## 🇹🇷 Türkçe – Türkçe Kılavuz

**BruteAI**, web içeriklerinden yapay zeka yardımıyla hedef odaklı ve etkili wordlist (şifre listesi) oluşturmanızı sağlar.

### 🚀 Özellikler

  - Yapay zeka tabanlı içerik analizi
  - Cloudflare gibi korumaları aşabilen gelişmiş crawler
  - **Otomatik dil tespiti** ile doğru analiz
  - CUDA bellek hatalarına karşı quantization
  - Çapraz platform (Windows/macOS/Linux) uyumlu
  - Otomatik donanım tespiti ve model ayarı
  - **Otomatik dosya isimlendirme** (ör: `ornek.com_username_wordlist.txt`)

### 🔧 Kurulum

Gerekli kütüphaneleri yüklemek için projenin ana dizininde aşağıdaki komutu çalıştırın:

```bash
pip install -r requirements.txt
```

### 🛠️ Kullanım

Aracı terminal üzerinden, hedef site adresini doğrudan yazarak çalıştırabilirsiniz.

```bash
python bruteai.py "https://ornek.com" --max-pages 10
```

**Parametreler:**
| Parametre | Açıklama | Tür | Varsayılan |
| :--- | :--- | :--- | :--- |
| `url` | **(Zorunlu)** Taranacak web sitesinin tam adresi. | metin | Yok |
| `--max-pages` | *(İsteğe Bağlı)* Taranacak maksimum sayfa sayısı. | sayı | `50` |
| `--snippet-length` | *(İsteğe Bağlı)* AI'a gönderilecek metin parçası uzunluğu. | sayı | `15000`|
| `--max-gen-tokens`| *(İsteğe Bağlı)* AI'ın üreteceği maksimum kelime sayısı. | sayı | `512` |

## 🇩🇪 Deutsch – Deutsche Anleitung

**BruteAI** ist ein KI-gestütztes Tool zur Erstellung gezielter und effektiver Wordlists aus Webseiteninhalten.

### 🚀 Funktionen

  - KI-basierte Inhaltsanalyse
  - Fortschrittlicher Crawler, der Schutzmaßnahmen wie Cloudflare umgeht
  - **Automatische Spracherkennung** für genaue Analysen
  - Quantisierung zur Reduzierung von CUDA-Speicherfehlern
  - Plattformübergreifende Kompatibilität
  - Automatische Hardware-Erkennung und Modellauswahl
  - **Automatische Dateibenennung** (z.B. `beispiel.de_username_wordlist.txt`)

### 🔧 Installation

Um die erforderlichen Python-Bibliotheken zu installieren, führen Sie den folgenden Befehl im Stammverzeichnis des Projekts aus:

```bash
pip install -r requirements.txt
```

### 🛠️ Nutzung

Sie können das Tool vom Terminal aus ausführen, indem Sie die Adresse der Zielseite direkt angeben.

```bash
python bruteai.py "https://beispiel.de" --max-pages 10
```

**Parameter:**
| Parameter | Beschreibung | Typ | Standard |
| :--- | :--- | :--- | :--- |
| `url` | **(Erforderlich)** Die vollständige Adresse der zu crawlenden Website. | Zeichenkette | Keine |
| `--max-pages` | *(Optional)* Maximale Anzahl der zu crawlenden Seiten. | Ganzzahl | `50` |
| `--snippet-length` | *(Optional)* Länge des an die KI gesendeten Textausschnitts. | Ganzzahl | `15000` |
| `--max-gen-tokens`| *(Optional)* Maximale Anzahl der von der KI zu generierenden Tokens. | Ganzzahl | `512` |
