FROM python:3.12.3-slim-bullseye

WORKDIR /usr/src/app
RUN chmod 777 /usr/src/app

# প্রয়োজনীয় প্যাকেজ ইনস্টল
RUN apt-get update -qq && apt-get install -y \
    git wget pv jq python3-dev mediainfo gcc aria2 \
    libsm6 libxext6 libfontconfig1 libxrender1 libgl1-mesa-glx ffmpeg \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY . .

# pip & setuptools আপডেট ও requirements ইনস্টল
RUN pip install --no-cache-dir --upgrade pip setuptools setuptools_scm wheel \
    && pip install --no-cache-dir -r requirements.txt

CMD ["bash", "run.sh"]
