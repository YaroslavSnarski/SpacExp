# официальный образ Python 3.11
FROM python:3.11

# необходимые пакеты для apt
RUN apt-get update --allow-unauthenticated --fix-missing && apt-get install -y --no-install-recommends \
    apt-utils \
    && rm -rf /var/lib/apt/lists/*

# системные зависимости, включая библиотеки OpenGL
RUN apt-get update && apt-get install -y --fix-missing \
    libgl1-mesa-glx \
    libglib2.0-0 \
#    pandoc \
    python3-pip \
    python3-dev \
    build-essential \
    libopencv-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y libreoffice

# рабочая директория app в контейнере
WORKDIR /app

# requirements.txt для установки зависимостей
COPY requirements.txt /app/

# зависимости из requirements.txt
RUN pip install -r requirements.txt --verbose

# весь проект (SpacExpWeb и SpacExp) в контейнер
COPY SpacExpWeb /app/SpacExpWeb
COPY SpacExp /app/SpacExp

# порт для Django
EXPOSE 8000

# команда для запуска сервера Django
CMD ["python", "SpacExpWeb/manage.py", "runserver", "0.0.0.0:8000"]
