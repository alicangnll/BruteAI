# 🔐 BruteAI – AI Destekli Wordlist Üretici

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

## 🇫🇷 Français – Guide Français

**BruteAI** est un outil basé sur l’IA qui permet de générer des wordlists ciblées à partir de contenu web.

### 🚀 Fonctionnalités

  - Analyse de contenu basée sur l'IA
  - Crawler avancé contournant les protections comme Cloudflare
  - **Détection automatique de la langue** pour une analyse précise
  - Quantification pour réduire les erreurs de mémoire CUDA
  - Compatibilité multiplateforme
  - Détection automatique du matériel et sélection du modèle
  - **Nommage automatique des fichiers** (ex: `exemple.fr_username_wordlist.txt`)

### 🔧 Installation

Exécutez la commande suivante pour installer les bibliothèques Python requises dans le répertoire racine du projet :

```bash
pip install -r requirements.txt
```

### 🛠️ Utilisation

Vous pouvez exécuter l'outil depuis le terminal en fournissant directement l'adresse du site cible.

```bash
python bruteai.py "https://exemple.fr" --max-pages 10
```

**Paramètres:**
| Paramètre | Description | Type | Défaut |
| :--- | :--- | :--- | :--- |
| `url` | **(Requis)** L'adresse complète du site à explorer. | chaîne | Aucun |
| `--max-pages` | *(Optionnel)* Nombre maximum de pages à explorer. | entier | `50` |
| `--snippet-length` | *(Optionnel)* Longueur de l'extrait de texte envoyé à l'IA. | entier | `15000` |
| `--max-gen-tokens`| *(Optionnel)* Nombre maximum de jetons à générer par l'IA. | entier | `512` |

## 🇪🇸 Español – Guía en Español

**BruteAI** es una herramienta de IA para generar listas de palabras eficaces a partir del contenido de un sitio web.

### 🚀 Características

  - Análisis de contenido basado en IA
  - Crawler avanzado que evita protecciones como Cloudflare
  - **Detección automática de idioma** para un análisis preciso
  - Cuantización para reducir errores de memoria CUDA
  - Compatibilidad multiplataforma
  - Detección automática de hardware y selección de modelo
  - **Nomenclatura automática de archivos** (ej: `ejemplo.es_username_wordlist.txt`)

### 🔧 Instalación

Para instalar las bibliotecas de Python requeridas, ejecute el siguiente comando en el directorio raíz del proyecto:

```bash
pip install -r requirements.txt
```

### 🛠️ Uso

Puede ejecutar la herramienta desde la terminal proporcionando la dirección del sitio de destino directamente.

```bash
python bruteai.py "https://ejemplo.es" --max-pages 10
```

**Parámetros:**
| Parámetro | Descripción | Tipo | Predeterminado |
| :--- | :--- | :--- | :--- |
| `url` | **(Requerido)** La dirección completa del sitio web a rastrear. | texto | Ninguno |
| `--max-pages` | *(Opcional)* Número máximo de páginas a rastrear. | número | `50` |
| `--snippet-length` | *(Opcional)* Longitud del fragmento de texto enviado a la IA. | número | `15000` |
| `--max-gen-tokens`| *(Opcional)* Número máximo de tokens que generará la IA. | número | `512` |

## 🇵🇹 Português – Guia em Português

**BruteAI** é uma ferramenta de IA que gera listas de palavras direcionadas a partir de conteúdo da web.

### 🚀 Recursos

  - Análise de conteúdo baseada em IA
  - Crawler avançado que contorna proteções como o Cloudflare
  - **Detecção automática de idioma** para análise precisa
  - Quantização para reduzir erros de memória CUDA
  - Compatível com Windows, macOS e Linux
  - Detecção automática de hardware e seleção do modelo
  - **Nomenclatura automática de arquivos** (ex: `exemplo.pt_username_wordlist.txt`)

### 🔧 Instalação

Para instalar as bibliotecas Python necessárias, execute o seguinte comando no diretório raiz do projeto:

```bash
pip install -r requirements.txt
```

### 🛠️ Uso

Você pode executar a ferramenta a partir do terminal, fornecendo o endereço do site de destino diretamente.

```bash
python bruteai.py "https://exemplo.pt" --max-pages 10
```

**Parâmetros:**
| Parâmetro | Descrição | Tipo | Padrão |
| :--- | :--- | :--- | :--- |
| `url` | **(Obrigatório)** O endereço completo do site a ser rastreado. | texto | Nenhum |
| `--max-pages` | *(Opcional)* Número máximo de páginas a rastrear. | número | `50` |
| `--snippet-length` | *(Opcional)* Comprimento do trecho de texto enviado à IA. | número | `15000` |
| `--max-gen-tokens`| *(Opcional)* Número máximo de tokens a serem gerados pela IA. | número | `512` |

## 🇷🇺 Русский – Русское руководство

**BruteAI** — это инструмент на основе ИИ для создания целевых словарей из веб-контента.

### 🚀 Возможности

  - Анализ содержимого с использованием ИИ
  - Продвинутый краулер, обходящий защиты вроде Cloudflare
  - **Автоматическое определение языка** для точного анализа
  - Квантование для снижения ошибок памяти CUDA
  - Кроссплатформенная совместимость
  - Автоматическое определение конфигурации системы и выбор модели
  - **Автоматическое именование файлов** (например, `primer.ru_username_wordlist.txt`)

### 🔧 Установка

Для установки необходимых библиотек Python выполните следующую команду в корневом каталоге проекта:

```bash
pip install -r requirements.txt
```

### 🛠️ Использование

Вы можете запустить инструмент из терминала, напрямую указав адрес целевого сайта.

```bash
python bruteai.py "https://primer.ru" --max-pages 10
```

**Параметры:**
| Параметр | Описание | Тип | По умолчанию |
| :--- | :--- | :--- | :--- |
| `url` | **(Обязательно)** Полный адрес веб-сайта для сканирования. | строка | Нет |
| `--max-pages` | *(Необязательно)* Максимальное количество страниц для сканирования. | число | `50` |
| `--snippet-length` | *(Необязательно)* Длина фрагмента текста, отправляемого в ИИ. | число | `15000` |
| `--max-gen-tokens`| *(Необязательно)* Максимальное количество токенов для генерации ИИ. | число | `512` |
