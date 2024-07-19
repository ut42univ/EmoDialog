FROM python:3
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

# Litestreamのインストール
RUN apt-get update && apt-get install -y curl \
    && curl -L https://github.com/benbjohnson/litestream/releases/latest/download/litestream-linux-amd64.tar.gz | tar xz \
    && mv litestream /usr/local/bin \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Litestreamの設定ファイルをコピー
COPY litestream.yml /etc/litestream.yml


# Run the web service on container startup.
CMD ["litestream", "replicate", "--config", "/etc/litestream.yml", "python", "app.py"]
