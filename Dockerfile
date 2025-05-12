# Используем базовый образ Python 3.11
FROM python:3.11

# Устанавливаем рабочую директорию
WORKDIR /usr/src/app

ADD ./app/requirements.txt /usr/src/app/requirements.txt

RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r /usr/src/app/requirements.txt

# Устанавливаем системные зависимости
RUN apt-get update && \
    apt-get install -y \
    wget \
    unzip \
    gnupg2 \
    curl \
    gettext \
    nano \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

ADD ./app /usr/src/app
ADD ./.env /usr/src/app/.env

RUN mkdir -p /dev/shm && chmod 1777 /dev/shm
