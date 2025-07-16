FROM python:3.12.3

# কাজের ডিরেক্টরি সেট করা
WORKDIR /usr/src/app

# পারমিশন দেওয়া
RUN chmod 777 /usr/src/app

# সিস্টেম প্যাকেজ ইনস্টল করা
RUN apt-get -qq update && apt-get -qq install -y \
    git wget pv jq python3-dev mediainfo gcc aria2 \
    libsm6 libxext6 libfontconfig1 libxrender1 libgl1-mesa-glx ffmpeg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# সোর্স কোড কপি করা
COPY . .

# pip, setuptools, wheel আপডেট + প্যাকেজ ইনস্টল
RUN pip install --no-cache-dir --upgrade pip setuptools setuptools_scm wheel \
    && pip install --no-cache-dir -r requirements.txt

# রান করার কমান্ড
CMD ["bash", "run.sh"]
