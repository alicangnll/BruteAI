# 🔐 BruteAI – AI-powered Wordlist Generator

## 🇬🇧 English Guide

**BruteAI** is an AI-powered tool that helps you generate targeted and effective wordlists from website content. It intelligently crawls a target website, analyzes its content using large language models, and extracts potential usernames and passwords.

### 🚀 Features

  - AI-based content analysis
  - Advanced crawler that bypasses protections like Cloudflare
  - **Automatic language detection** for accurate analysis
  - **Custom Model Support:** Ability to use any public model from Hugging Face.
  - **Rate Limiting:** Controls for request frequency to avoid blocking.
  - Quantization to reduce CUDA memory errors
  - Cross-platform (Windows/macOS/Linux) compatibility
  - Automatic hardware detection and model selection
  - **Automatic file naming** (e.g., `example.com_username_wordlist.txt`)

### 🔧 Installation

1.  **Install Google Chrome:** The advanced crawler requires Google Chrome. Please ensure it is installed on your system.

2.  Install the required Python libraries by running the following command in the project's root directory:

    ```bash
    pip install -r requirements.txt
    ```

### 🛠️ Usage

#### Basic Usage

You can run the tool from the terminal by providing the target site address.

```bash
python bruteai.py "https://example.com"
```

#### Advanced Usage

Run with more specific parameters, like setting a page limit, specifying a custom AI model, and controlling the crawl speed.

```bash
python bruteai.py "https://target-site.com" --max-pages 20 --custom-model-name "deepseek-ai/deepseek-coder-1.3b-instruct" --sleep-between-requests 2
```

**Parameters:**
| Parameter | Description | Type | Default |
| :--- | :--- | :--- | :--- |
| `url` | **(Required)** The full address of the website to crawl. | string | None |
| `--max-pages` | *(Optional)* Maximum number of pages to crawl. | integer | `None` (No limit) |
| `--requests-per-second`| *(Optional)* Max requests per second (rate limiting). | float | `None` |
| `--sleep-between-requests`| *(Optional)* Seconds to wait between requests. | float | `None` |
| `--snippet-length` | *(Optional)* Length of the text snippet sent to the AI. | integer | `15000` |
| `--max-gen-tokens`| *(Optional)* Maximum number of tokens for the AI to generate. | integer | `512` |
| `--custom-model-name`| *(Optional)* Custom model name from Hugging Face. | string | `None` |

## 🇹🇷 Türkçe Kılavuz

**BruteAI**, web içeriklerinden yapay zeka yardımıyla hedef odaklı ve etkili wordlist (şifre listesi) oluşturmanızı sağlar. Hedef web sitesini akıllıca tarar, içeriğini büyük dil modelleri kullanarak analiz eder ve potansiyel kullanıcı adı ve parolaları çıkarır.

### 🚀 Özellikler

  - Yapay zeka tabanlı içerik analizi
  - Cloudflare gibi korumaları aşabilen gelişmiş crawler
  - **Otomatik dil tespiti** ile doğru analiz
  - **Özel Model Desteği:** Hugging Face üzerinden herhangi bir açık modeli kullanma imkanı.
  - **Hız Sınırlama (Rate Limiting):** Engellenmeyi önlemek için istek frekansı kontrolleri.
  - CUDA bellek hatalarına karşı quantization
  - Çapraz platform (Windows/macOS/Linux) uyumlu
  - Otomatik donanım tespiti ve model ayarı
  - **Otomatik dosya isimlendirme** (ör: `ornek.com_username_wordlist.txt`)

### 🔧 Kurulum

1.  **Google Chrome Kurulumu:** Gelişmiş crawler, Google Chrome gerektirir. Lütfen sisteminizde kurulu olduğundan emin olun.

2.  Gerekli kütüphaneleri yüklemek için projenin ana dizininde aşağıdaki komutu çalıştırın:

    ```bash
    pip install -r requirements.txt
    ```

### 🛠️ Kullanım

#### Temel Kullanım

Aracı terminal üzerinden, hedef site adresini doğrudan yazarak çalıştırabilirsiniz.

```bash
python bruteai.py "https://ornek.com"
```

#### Gelişmiş Kullanım

Sayfa limiti belirleme, özel bir AI modeli kullanma ve tarama hızını kontrol etme gibi daha spesifik parametrelerle çalıştırın.

```bash
python bruteai.py "https://hedef-site.com" --max-pages 20 --custom-model-name "deepseek-ai/deepseek-coder-1.3b-instruct" --sleep-between-requests 2
```

**Parametreler:**
| Parametre | Açıklama | Tür | Varsayılan |
| :--- | :--- | :--- | :--- |
| `url` | **(Zorunlu)** Taranacak web sitesinin tam adresi. | metin | Yok |
| `--max-pages` | *(İsteğe Bağlı)* Taranacak maksimum sayfa sayısı. | sayı | `Yok` (Limitsiz) |
| `--requests-per-second`| *(İsteğe Bağlı)* Saniye başına maksimum istek (hız sınırlama). | ondalık sayı | `Yok` |
| `--sleep-between-requests`| *(İsteğe Bağlı)* İstekler arasında beklenecek süre (sn).| ondalık sayı | `Yok` |
| `--snippet-length` | *(İsteğe Bağlı)* AI'a gönderilecek metin parçası uzunluğu. | sayı | `15000`|
| `--max-gen-tokens`| *(İsteğe Bağlı)* AI'ın üreteceği maksimum token sayısı. | sayı | `512` |
| `--custom-model-name`| *(İsteğe Bağlı)* Hugging Face'den özel model adı. | metin | `Yok` |

## 🇩🇪 Deutsche Anleitung

**BruteAI** ist ein KI-gestütztes Tool, das Ihnen hilft, gezielte und effektive Wordlists aus Webseiteninhalten zu erstellen. Es durchsucht intelligent eine Ziel-Website, analysiert deren Inhalt mithilfe großer Sprachmodelle und extrahiert potenzielle Benutzernamen und Passwörter.

### 🚀 Funktionen

  - KI-basierte Inhaltsanalyse
  - Fortschrittlicher Crawler, der Schutzmaßnahmen wie Cloudflare umgeht
  - **Automatische Spracherkennung** für genaue Analysen
  - **Unterstützung für benutzerdefinierte Modelle:** Möglichkeit, jedes öffentliche Modell von Hugging Face zu verwenden.
  - **Rate-Limiting:** Kontrollen für die Anfragefrequenz, um Sperrungen zu vermeiden.
  - Quantisierung zur Reduzierung von CUDA-Speicherfehlern
  - Plattformübergreifende Kompatibilität
  - Automatische Hardware-Erkennung und Modellauswahl
  - **Automatische Dateibenennung** (z.B. `beispiel.de_username_wordlist.txt`)

### 🔧 Installation

1.  **Google Chrome installieren:** Der fortschrittliche Crawler erfordert Google Chrome. Bitte stellen Sie sicher, dass es auf Ihrem System installiert ist.

2.  Um die erforderlichen Python-Bibliotheken zu installieren, führen Sie den folgenden Befehl im Stammverzeichnis des Projekts aus:

    ```bash
    pip install -r requirements.txt
    ```

### 🛠️ Nutzung

#### Grundlegende Nutzung

Sie können das Tool vom Terminal aus ausführen, indem Sie die Adresse der Zielseite angeben.

```bash
python bruteai.py "https://beispiel.de"
```

#### Erweiterte Nutzung

Führen Sie es mit spezifischeren Parametern aus, wie z. B. dem Festlegen eines Seitenlimits, der Angabe eines benutzerdefinierten KI-Modells und der Steuerung der Crawl-Geschwindigkeit.

```bash
python bruteai.py "https://ziel-seite.de" --max-pages 20 --custom-model-name "deepseek-ai/deepseek-coder-1.3b-instruct" --sleep-between-requests 2
```

**Parameter:**
| Parameter | Beschreibung | Typ | Standard |
| :--- | :--- | :--- | :--- |
| `url` | **(Erforderlich)** Die vollständige Adresse der zu crawlenden Website. | Zeichenkette | Keine |
| `--max-pages` | *(Optional)* Maximale Anzahl der zu crawlenden Seiten. | Ganzzahl | `Keine` (Unbegrenzt) |
| `--requests-per-second`| *(Optional)* Max. Anfragen pro Sekunde (Rate-Limiting). | Gleitkommazahl | `Keine` |
| `--sleep-between-requests`| *(Optional)* Sekunden, die zwischen Anfragen gewartet werden.| Gleitkommazahl | `Keine` |
| `--snippet-length` | *(Optional)* Länge des an die KI gesendeten Textausschnitts. | Ganzzahl | `15000` |
| `--max-gen-tokens`| *(Optional)* Maximale Anzahl der von der KI zu generierenden Tokens. | Ganzzahl | `512` |
| `--custom-model-name`| *(Optional)* Benutzerdefinierter Modellname von Hugging Face.| Zeichenkette | `Keine` |

## 🇫🇷 Guide Français

**BruteAI** est un outil basé sur l’IA qui vous aide à générer des wordlists ciblées et efficaces à partir du contenu de sites web. Il explore intelligemment un site web cible, analyse son contenu à l'aide de grands modèles de langage et en extrait des noms d'utilisateur et des mots de passe potentiels.

### 🚀 Fonctionnalités

  - Analyse de contenu basée sur l'IA
  - Crawler avancé contournant les protections comme Cloudflare
  - **Détection automatique de la langue** pour une analyse précise
  - **Prise en charge des modèles personnalisés :** Possibilité d'utiliser n'importe quel modèle public de Hugging Face.
  - **Limitation de débit (Rate Limiting) :** Contrôles de la fréquence des requêtes pour éviter le blocage.
  - Quantification pour réduire les erreurs de mémoire CUDA
  - Compatibilité multiplateforme
  - Détection automatique du matériel et sélection du modèle
  - **Nommage automatique des fichiers** (ex: `exemple.fr_username_wordlist.txt`)

### 🔧 Installation

1.  **Installez Google Chrome :** Le crawler avancé nécessite Google Chrome. Veuillez vous assurer qu'il est installé sur votre système.

2.  Exécutez la commande suivante pour installer les bibliothèques Python requises dans le répertoire racine du projet :

    ```bash
    pip install -r requirements.txt
    ```

### 🛠️ Utilisation

#### Utilisation de base

Vous pouvez exécuter l'outil depuis le terminal en fournissant directement l'adresse du site cible.

```bash
python bruteai.py "https://exemple.fr"
```

#### Utilisation avancée

Exécutez avec des paramètres plus spécifiques, comme définir une limite de pages, spécifier un modèle d'IA personnalisé et contrôler la vitesse d'exploration.

```bash
python bruteai.py "https://site-cible.fr" --max-pages 20 --custom-model-name "deepseek-ai/deepseek-coder-1.3b-instruct" --sleep-between-requests 2
```

**Paramètres:**
| Paramètre | Description | Type | Défaut |
| :--- | :--- | :--- | :--- |
| `url` | **(Requis)** L'adresse complète du site à explorer. | chaîne | Aucun |
| `--max-pages` | *(Optionnel)* Nombre maximum de pages à explorer. | entier | `Aucun` (Sans limite) |
| `--requests-per-second`| *(Optionnel)* Nombre max de requêtes par seconde. | flottant | `Aucun` |
| `--sleep-between-requests`| *(Optionnel)* Secondes d'attente entre les requêtes.| flottant | `Aucun` |
| `--snippet-length` | *(Optionnel)* Longueur de l'extrait de texte envoyé à l'IA. | entier | `15000` |
| `--max-gen-tokens`| *(Optionnel)* Nombre maximum de tokens à générer par l'IA. | entier | `512` |
| `--custom-model-name`| *(Optionnel)* Nom du modèle personnalisé de Hugging Face.| chaîne | `Aucun` |

## 🇪🇸 Guía en Español

**BruteAI** es una herramienta de IA que le ayuda a generar listas de palabras específicas y eficaces a partir del contenido de un sitio web. Rastrea de forma inteligente un sitio web de destino, analiza su contenido mediante grandes modelos lingüísticos y extrae posibles nombres de usuario y contraseñas.

### 🚀 Características

  - Análisis de contenido basado en IA
  - Crawler avanzado que evita protecciones como Cloudflare
  - **Detección automática de idioma** para un análisis preciso
  - **Soporte para modelos personalizados:** Capacidad para usar cualquier modelo público de Hugging Face.
  - **Limitación de velocidad (Rate Limiting):** Controles para la frecuencia de solicitudes para evitar bloqueos.
  - Cuantización para reducir errores de memoria CUDA
  - Compatibilidad multiplataforma
  - Detección automática de hardware y selección de modelo
  - **Nomenclatura automática de archivos** (ej: `ejemplo.es_username_wordlist.txt`)

### 🔧 Instalación

1.  **Instale Google Chrome:** El crawler avanzado requiere Google Chrome. Por favor, asegúrese de que está instalado en su sistema.

2.  Para instalar las bibliotecas de Python requeridas, ejecute el siguiente comando en el directorio raíz del proyecto:

    ```bash
    pip install -r requirements.txt
    ```

### 🛠️ Uso

#### Uso básico

Puede ejecutar la herramienta desde la terminal proporcionando la dirección del sitio de destino.

```bash
python bruteai.py "https://ejemplo.es"
```

#### Uso avanzado

Ejecute con parámetros más específicos, como establecer un límite de páginas, especificar un modelo de IA personalizado y controlar la velocidad de rastreo.

```bash
python bruteai.py "https://sitio-objetivo.es" --max-pages 20 --custom-model-name "deepseek-ai/deepseek-coder-1.3b-instruct" --sleep-between-requests 2
```

**Parámetros:**
| Parámetro | Descripción | Tipo | Predeterminado |
| :--- | :--- | :--- | :--- |
| `url` | **(Requerido)** La dirección completa del sitio web a rastrear. | texto | Ninguno |
| `--max-pages` | *(Opcional)* Número máximo de páginas a rastrear. | número | `Ninguno` (Sin límite) |
| `--requests-per-second`| *(Opcional)* Máximo de solicitudes por segundo. | flotante | `Ninguno` |
| `--sleep-between-requests`| *(Opcional)* Segundos de espera entre solicitudes.| flotante | `Ninguno` |
| `--snippet-length` | *(Opcional)* Longitud del fragmento de texto enviado a la IA. | número | `15000` |
| `--max-gen-tokens`| *(Opcional)* Número máximo de tokens que generará la IA. | número | `512` |
| `--custom-model-name`| *(Opcional)* Nombre del modelo personalizado de Hugging Face.| texto | `Ninguno` |

## 🇵🇹 Guia em Português

**BruteAI** é uma ferramenta de IA que o ajuda a gerar listas de palavras direcionadas e eficazes a partir do conteúdo de websites. Ele rastreia de forma inteligente um site alvo, analisa seu conteúdo usando grandes modelos de linguagem e extrai potenciais nomes de usuário e senhas.

### 🚀 Recursos

  - Análise de conteúdo baseada em IA
  - Crawler avançado que contorna proteções como o Cloudflare
  - **Detecção automática de idioma** para análise precisa
  - **Suporte a Modelos Personalizados:** Capacidade de usar qualquer modelo público do Hugging Face.
  - **Limitação de Taxa (Rate Limiting):** Controlos para a frequência de pedidos para evitar bloqueios.
  - Quantização para reduzir erros de memória CUDA
  - Compatível com Windows, macOS e Linux
  - Detecção automática de hardware e seleção do modelo
  - **Nomenclatura automática de arquivos** (ex: `exemplo.pt_username_wordlist.txt`)

### 🔧 Instalação

1.  **Instale o Google Chrome:** O crawler avançado requer o Google Chrome. Por favor, certifique-se de que está instalado no seu sistema.

2.  Para instalar as bibliotecas Python necessárias, execute o seguinte comando no diretório raiz do projeto:

    ```bash
    pip install -r requirements.txt
    ```

### 🛠️ Uso

#### Uso Básico

Você pode executar a ferramenta a partir do terminal, fornecendo o endereço do site de destino.

```bash
python bruteai.py "https://exemplo.pt"
```

#### Uso Avançado

Execute com parâmetros mais específicos, como definir um limite de páginas, especificar um modelo de IA personalizado e controlar a velocidade de rastreamento.

```bash
python bruteai.py "https://site-alvo.pt" --max-pages 20 --custom-model-name "deepseek-ai/deepseek-coder-1.3b-instruct" --sleep-between-requests 2
```

**Parâmetros:**
| Parâmetro | Descrição | Tipo | Padrão |
| :--- | :--- | :--- | :--- |
| `url` | **(Obrigatório)** O endereço completo do site a ser rastreado. | texto | Nenhum |
| `--max-pages` | *(Opcional)* Número máximo de páginas a rastrear. | número | `Nenhum` (Sem limite) |
| `--requests-per-second`| *(Opcional)* Máximo de pedidos por segundo. | flutuante | `Nenhum` |
| `--sleep-between-requests`| *(Opcional)* Segundos a aguardar entre os pedidos.| flutuante | `Nenhum` |
| `--snippet-length` | *(Opcional)* Comprimento do trecho de texto enviado à IA. | número | `15000` |
| `--max-gen-tokens`| *(Opcional)* Número máximo de tokens a serem gerados pela IA. | número | `512` |
| `--custom-model-name`| *(Opcional)* Nome do modelo personalizado do Hugging Face.| texto | `Nenhum` |

## 🇷🇺 Русское руководство

**BruteAI** — это инструмент на базе ИИ, который помогает создавать целевые и эффективные словари из веб-контента. Он интеллектуально сканирует целевой веб-сайт, анализирует его содержимое с помощью больших языковых моделей и извлекает потенциальные имена пользователей и пароли.

### 🚀 Возможности

  - Анализ содержимого с использованием ИИ
  - Продвинутый краулер, обходящий защиты вроде Cloudflare
  - **Автоматическое определение языка** для точного анализа
  - **Поддержка пользовательских моделей:** Возможность использовать любую публичную модель с Hugging Face.
  - **Ограничение скорости запросов (Rate Limiting):** Контроль частоты запросов для избежания блокировки.
  - Квантование для снижения ошибок памяти CUDA
  - Кроссплатформенная совместимость
  - Автоматическое определение конфигурации системы и выбор модели
  - **Автоматическое именование файлов** (например, `primer.ru_username_wordlist.txt`)

### 🔧 Установка

1.  **Установите Google Chrome:** Для работы продвинутого краулера требуется Google Chrome. Пожалуйста, убедитесь, что он установлен в вашей системе.

2.  Для установки необходимых библиотек Python выполните следующую команду в корневом каталоге проекта:

    ```bash
    pip install -r requirements.txt
    ```

### 🛠️ Использование

#### Базовое использование

Вы можете запустить инструмент из терминала, указав адрес целевого сайта.

```bash
python bruteai.py "https://primer.ru"
```

#### Расширенное использование

Запустите с более конкретными параметрами, такими как установка лимита страниц, указание пользовательской модели ИИ и контроль скорости сканирования.

```bash
python bruteai.py "https://целевой-сайт.рф" --max-pages 20 --custom-model-name "deepseek-ai/deepseek-coder-1.3b-instruct" --sleep-between-requests 2
```

**Параметры:**
| Параметр | Описание | Тип | По умолчанию |
| :--- | :--- | :--- | :--- |
| `url` | **(Обязательно)** Полный адрес веб-сайта для сканирования. | строка | Нет |
| `--max-pages` | *(Необязательно)* Максимальное количество страниц для сканирования. | число | `Нет` (Без ограничений) |
| `--requests-per-second`| *(Необязательно)* Макс. запросов в секунду (ограничение скорости). | дробное | `Нет` |
| `--sleep-between-requests`| *(Необязательно)* Время ожидания между запросами (в сек).| дробное | `Нет` |
| `--snippet-length` | *(Необязательно)* Длина фрагмента текста, отправляемого в ИИ. | число | `15000` |
| `--max-gen-tokens`| *(Необязательно)* Максимальное количество токенов для генерации ИИ. | число | `512` |
| `--custom-model-name`| *(Необязательно)* Имя пользовательской модели из Hugging Face.| строка | `Нет` |

## IMPORTANT NOTE!

### 🇬🇧 English
**Disclaimer:** This tool is provided for educational purposes and for use in authorized security testing environments only. It is intended to help security professionals, researchers, and students understand how context-specific wordlists can be generated. You must have explicit, written permission from the system owner before using this tool on any target. Any actions and or activities related to the use of this tool are solely your responsibility. The misuse of this information can result in criminal charges brought against the persons in question. The author assumes no liability and is not responsible for any misuse or damage caused by this tool.

### 🇹🇷 Türkçe
**Sorumluluk Reddi:** Bu araç, yalnızca eğitim amaçlı ve yetkilendirilmiş güvenlik testi ortamlarında kullanılmak üzere sağlanmıştır. Güvenlik uzmanlarının, araştırmacıların ve öğrencilerin bağlama özgü kelime listelerinin nasıl oluşturulabileceğini anlamalarına yardımcı olmayı amaçlamaktadır. Herhangi bir hedef sistemde bu aracı kullanmadan önce sistem sahibinden açık ve yazılı izin almanız gerekmektedir. Bu aracın kullanımıyla ilgili her türlü eylem ve faaliyet tamamen sizin sorumluluğunuzdadır. Bu bilgilerin kötüye kullanılması, ilgili kişiler hakkında cezai suçlamalara yol açabilir. Yazar, bu aracın neden olduğu herhangi bir kötüye kullanım veya zarardan dolayı hiçbir yükümlülük kabul etmez ve sorumlu değildir.

### 🇩🇪 Deutsch
**Haftungsausschluss:** Dieses Tool wird ausschließlich zu Bildungszwecken und zur Verwendung in autorisierten Sicherheitstestumgebungen zur Verfügung gestellt. Es soll Sicherheitsexperten, Forschern und Studenten helfen zu verstehen, wie kontextspezifische Wortlisten generiert werden können. Sie müssen eine ausdrückliche, schriftliche Genehmigung des Systembesitzers einholen, bevor Sie dieses Tool auf einem Zielsystem verwenden. Alle Handlungen und Aktivitäten im Zusammenhang mit der Nutzung dieses Tools liegen allein in Ihrer Verantwortung. Der Missbrauch dieser Informationen kann zu strafrechtlichen Anklagen gegen die betreffenden Personen führen. Der Autor übernimmt keine Haftung und ist nicht für Missbrauch oder Schäden verantwortlich, die durch dieses Tool verursacht werden.

### 🇫🇷 Français
**Avis de non-responsabilité :** Cet outil est fourni à des fins éducatives et pour une utilisation dans des environnements de test de sécurité autorisés uniquement. Il est destiné à aider les professionnels de la sécurité, les chercheurs et les étudiants à comprendre comment des listes de mots spécifiques à un contexte peuvent être générées. Vous devez obtenir une autorisation écrite et explicite du propriétaire du système avant d'utiliser cet outil sur une cible. Toutes les actions et activités liées à l'utilisation de cet outil relèvent de votre seule responsabilité. L'utilisation abusive de ces informations peut entraîner des poursuites pénales contre les personnes concernées. L'auteur n'assume aucune responsabilité et n'est pas responsable de toute mauvaise utilisation ou de tout dommage causé par cet outil.

### 🇪🇸 Español
**Descargo de responsabilidad:** Esta herramienta se proporciona con fines educativos y para su uso exclusivo en entornos de pruebas de seguridad autorizados. Su objetivo es ayudar a profesionales de la seguridad, investigadores y estudiantes a comprender cómo se pueden generar listas de palabras específicas del contexto. Debe tener un permiso explícito y por escrito del propietario del sistema antes de utilizar esta herramienta en cualquier objetivo. Cualquier acción y/o actividad relacionada con el uso de esta herramienta es de su exclusiva responsabilidad. El uso indebido de esta información puede dar lugar a acciones penales contra las personas en cuestión. El autor no asume ninguna responsabilidad y no se hace responsable de ningún mal uso o daño causado por esta herramienta.

### 🇵🇹 Português
**Isenção de Responsabilidade:** Esta ferramenta é fornecida para fins educacionais e para uso exclusivo em ambientes de teste de segurança autorizados. Destina-se a ajudar profissionais de segurança, pesquisadores e estudantes a entender como listas de palavras específicas de contexto podem ser geradas. Você deve ter permissão explícita e por escrito do proprietário do sistema antes de usar esta ferramenta em qualquer alvo. Quaisquer ações e/ou atividades relacionadas ao uso desta ferramenta são de sua exclusiva responsabilidade. O uso indevido desta informação pode resultar em acusações criminais contra as pessoas em questão. O autor не assume qualquer responsabilidade e não é responsável por qualquer uso indevido ou dano causado por esta ferramenta.

### 🇷🇺 Русский
**Отказ от ответственности:** Этот инструмент предоставляется исключительно в образовательных целях и для использования в авторизованных средах тестирования безопасности. Он предназначен для помощи специалистам по безопасности, исследователям и студентам в понимании того, как могут быть созданы контекстно-зависимые списки слов. Вы должны получить явное письменное разрешение от владельца системы перед использованием этого инструмента на любой цели. Все действия и/или мероприятия, связанные с использованием этого инструмента, находятся исключительно под вашей ответственностью. Неправомерное использование этой информации может привести к уголовному преследованию соответствующих лиц. Автор не несет никакой ответственности и не отвечает за любое неправомерное использование или ущерб, причиненный этим инструментом.
