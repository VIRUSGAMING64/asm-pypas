FROM python:3.12-alpine

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apk add --no-cache \
    bash \
    nodejs \
    npm \
    g++ \
    libstdc++

COPY requirements.txt ./
RUN pip install -r requirements.txt

RUN npm install @babel/core @babel/preset-react

COPY . .

RUN g++ scripts/clean.cpp -O2 -o scripts/clean && chmod +x scripts/clean scripts/run.sh scripts/buildpage.sh

EXPOSE 8000

CMD ["bash", "scripts/run.sh"]
