# Advanced Web Scraper

Bu proje, gelişmiş özelliklere sahip, yüksek performanslı ve tespit edilmesi zor bir web scraper uygulamasıdır.

## Özellikler

- Asenkron çalışma (asyncio)
- Proxy yönetimi ve otomatik rotasyon
- Tor ağı desteği
- Captcha çözme yeteneği
- JavaScript rendering
- Stealth modu (tarayıcı parmak izi gizleme)
- Dağıtık scraping desteği
- Veri şifreleme ve sıkıştırma
- Gelişmiş hata yönetimi ve yeniden deneme mekanizması
- Yapılandırılabilir ayarlar

## Yeni Özellikler

### Gelişmiş Anti-Tespit Teknikleri

- **Gelişmiş Browser Fingerprinting**: WebGL, AudioContext ve Font fingerprinting'e karşı gelişmiş koruma.
- **Yapay Zeka Tabanlı Davranış Simülasyonu**: İnsan benzeri davranışları taklit etmek için makine öğrenimi modeli kullanımı.
- **Makine Öğrenimi Tabanlı Proxy Rotasyonu**: En uygun proxy'yi seçmek için akıllı bir sistem.

### Derin Öğrenme Tabanlı Captcha Çözücü

- Kendi eğitilmiş derin öğrenme modelini kullanarak captcha'ları çözer.
- API tabanlı çözücü ile yedekli çalışır.

### Dinamik JavaScript Analizi ve Manipülasyonu

- Sayfadaki JavaScript kodlarını otomatik olarak analiz eder.
- Anti-bot kontrollerini tespit eder ve devre dışı bırakmaya çalışır.
- JavaScript kodlarını dinamik olarak manipüle eder.

### Yapay Zeka Tabanlı İçerik Analizi

- Scrape edilen metinleri otomatik olarak analiz eder.
- Named Entity Recognition (NER) ile önemli varlıkları tespit eder.
- Metin özetleme özelliği ile uzun içerikleri özetler.
- Duygu analizi yaparak metnin genel tonunu belirler.
- Anahtar kelime çıkarımı ile metnin ana konularını tespit eder.

## Kurulum

1. Gerekli Python paketlerini yükleyin:

   ```
   pip install -r requirements.txt
   ```

2. Tor'u sisteminize kurun (isteğe bağlı, ancak önerilir):

   - Ubuntu: `sudo apt-get install tor`
   - macOS: `brew install tor`

3. `.env` dosyasını oluşturun ve gerekli ayarları yapın (örnek için `.env.example` dosyasına bakın).

4. Redis'i kurun ve çalıştırın (dağıtık scraping için gerekli):
   - Ubuntu: `sudo apt-get install redis-server`
   - macOS: `brew install redis`

## Kullanım

1. Ana scraper'ı çalıştırmak için:

   ```
   python main.py
   ```

2. Dağıtık scraping modunda çalıştırmak için:
   - `.env` dosyasında `USE_DISTRIBUTED_SCRAPING=True` olarak ayarlayın.
   - Redis sunucusunun çalıştığından emin olun.
   - Birden fazla terminal veya makinede `python main.py` komutunu çalıştırın.

## Yapılandırma

Tüm yapılandırma ayarları `.env` dosyasında bulunmaktadır. Önemli ayarlar şunlardır:

- `CAPTCHA_API_KEY`: 2captcha servisinden alınan API anahtarı
- `ENCRYPTION_KEY`: Veri şifreleme için kullanılan 32 byte'lık anahtar
- `TARGET_URLS`: Scrape edilecek URL'ler
- `USE_JS_RENDERING`: JavaScript rendering'i kullanıp kullanmama
- `USE_STEALTH_MODE`: Stealth modunu etkinleştirme
- `USE_DISTRIBUTED_SCRAPING`: Dağıtık scraping'i etkinleştirme
- `USE_ADVANCED_FINGERPRINT_EVASION`: Gelişmiş fingerprint gizleme tekniklerini etkinleştirir.
- `USE_AI_BEHAVIOR_SIMULATION`: Yapay zeka tabanlı davranış simülasyonunu etkinleştirir.
- `USE_ML_PROXY_ROTATION`: Makine öğrenimi tabanlı proxy rotasyonunu etkinleştirir.
- `CAPTCHA_MODEL_PATH`: Derin öğrenme captcha çözücü modelinin yolu
- `USE_DYNAMIC_JS_ANALYSIS`: Dinamik JavaScript analizi ve manipülasyonunu etkinleştirir.
- `USE_CONTENT_ANALYSIS`: Yapay zeka tabanlı içerik analizini etkinleştirir.

## Dosya Yapısı

- `main.py`: Ana giriş noktası
- `scraper.py`: Asenkron scraper sınıfı
- `proxy_manager.py`: Proxy yönetimi
- `tor_manager.py`: Tor ağı yönetimi
- `data_manager.py`: Veri şifreleme ve saklama
- `captcha_solver.py`: Captcha çözme işlemleri
- `config.py`: Yapılandırma yönetimi
- `distributed_scraper.py`: Dağıtık scraping işlemleri
- `stealth_utils.py`: Tarayıcı parmak izi gizleme yardımcıları

## Güvenlik ve Etik Kullanım

Bu scraper, araştırma ve eğitim amaçlı geliştirilmiştir. Kullanırken şunlara dikkat edin:

- Hedef sitelerin kullanım şartlarını ve robots.txt dosyalarını kontrol edin.
- Aşırı yük bindirmekten kaçının ve makul aralıklarla istek gönderin.
- Kişisel veya gizli bilgileri scrape etmeyin.
- Yasal ve etik sınırlar içinde kalın.

## Katkıda Bulunma

Hata raporları, özellik istekleri ve pull request'ler her zaman açıktır. Büyük değişiklikler için lütfen önce bir konu açın.

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için `LICENSE` dosyasına bakın.
