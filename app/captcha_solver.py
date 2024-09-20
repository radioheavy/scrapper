import tensorflow as tf
import numpy as np
import cv2
from io import BytesIO
from PIL import Image
import requests

class DeepLearningCaptchaSolver:
    def __init__(self, model_path):
        self.model = tf.keras.models.load_model(model_path)
        self.char_list = "0123456789abcdefghijklmnopqrstuvwxyz"

    def preprocess_image(self, image):
        # Görüntüyü ön işleme tabi tutun (boyutlandırma, normalizasyon vb.)
        image = cv2.resize(image, (200, 50))
        image = image / 255.0
        return image

    def decode_prediction(self, prediction):
        # Model çıktısını karakterlere dönüştürün
        out = ""
        for p in prediction:
            if np.argmax(p) < len(self.char_list):
                out += self.char_list[np.argmax(p)]
        return out

    async def solve(self, captcha_image):
        # Captcha görüntüsünü yükleyin ve ön işleme tabi tutun
        if isinstance(captcha_image, str):  # URL ise
            response = requests.get(captcha_image)
            img = Image.open(BytesIO(response.content))
        else:  # Dosya yolu ise
            img = Image.open(captcha_image)
        
        img = np.array(img)
        img = self.preprocess_image(img)
        
        # Modeli kullanarak tahmin yapın
        prediction = self.model.predict(np.expand_dims(img, axis=0))
        
        # Tahmini çözün ve döndürün
        solution = self.decode_prediction(prediction[0])
        return solution

class CaptchaSolver:
    def __init__(self, api_key, model_path):
        self.api_solver = TwoCaptcha(api_key)
        self.dl_solver = DeepLearningCaptchaSolver(model_path)

    def detect_captcha(self, soup):
        # Bu metod, sayfada captcha olup olmadığını kontrol eder
        # Hedef siteye göre özelleştirilmelidir
        return 'captcha' in soup.text.lower()

    async def solve(self, soup):
        try:
            # Önce derin öğrenme modelini kullanın
            captcha_img = soup.find('img', {'class': 'captcha'})['src']
            solution = await self.dl_solver.solve(captcha_img)
            if solution:
                return solution

            # Derin öğrenme başarısız olursa, API'yi kullanın
            site_key = soup.find('div', {'class': 'g-recaptcha'})['data-sitekey']
            result = await self.api_solver.recaptcha(sitekey=site_key, url=soup.url)
            return result
        except Exception as e:
            logger.error(f"Captcha çözümünde hata: {e}")
            return None

class TwoCaptcha:
    def __init__(self, api_key):
        self.api_key = api_key

    async def recaptcha(self, sitekey, url):
        # reCAPTCHA çözme isteği gönder
        request_url = f"http://2captcha.com/in.php?key={self.api_key}&method=userrecaptcha&googlekey={sitekey}&pageurl={url}"
        response = requests.get(request_url)
        if response.text.startswith('OK|'):
            captcha_id = response.text.split('|')[1]
            
            # Sonucu bekle ve al
            for _ in range(24):  # 2 dakika boyunca her 5 saniyede bir kontrol et
                await asyncio.sleep(5)
                result_url = f"http://2captcha.com/res.php?key={self.api_key}&action=get&id={captcha_id}"
                response = requests.get(result_url)
                if response.text.startswith('OK|'):
                    return response.text.split('|')[1]
        
        return None