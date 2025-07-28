apt-get update
apt-get install -y libwoff2-1 libwoff2dec1 libgstreamer-gl1.0-0 libharfbuzz-icu0 libenchant-2-2 libsecret-1-0 libhyphen0 libmanette-0.2-0 libavif13 libopus0 libwebpdemux2 libwebpmux3 libgstreamer-plugins-base1.0-0 libgstreamer-plugins-good1.0-0 libgstreamer1.0-0 gstreamer1.0-libav libgtk-3-0 python3 python3-pip
python3 -m pip install playwright transformers torch accelerate bitsandbytes PyMuPDF python-docx langdetect beautifulsoup4 requests --break-system-packages
python3 -m playwright install --with-deps chromium