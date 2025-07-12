FROM python:3.12.3-slim-buster

WORKDIR /usr/src/app
RUN chmod 777 /usr/src/app

RUN apt-get -qq update && apt-get -qq install -y git wget pv jq python3-dev mediainfo gcc aria2 libsm6 libxext6 libfontconfig1 libxrender1 libgl1-mesa-glx ffmpeg

COPY . .
# setuptools & pip আপডেট করে প্যাকেজ ইন্সটল করা (Error Fix করা হয়েছে)
RUN pip install --no-cache-dir --upgrade pip setuptools setuptools_scm wheel \
    && pip install --no-cache-dir -r requirements.txt

CMD ["bash","run.sh"]
