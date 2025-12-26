# Hafif bir Python imajı kullanıyoruz
FROM python:3.11-slim

# Logların anlık akması ve gereksiz .pyc dosyaları oluşmaması için ayarlar
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Çalışma dizinini ayarla
WORKDIR /app

# Önce gereksinimleri kopyala ve kur (Cache avantajı için)
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Proje dosyalarını kopyala
COPY . /app/

# Waitress ile projeyi ayağa kaldır
CMD ["waitress-serve", "--listen=0.0.0.0:8000", "core.wsgi:application"]