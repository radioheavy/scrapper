from cryptography.fernet import Fernet
import json
import os
import gzip

class DataManager:
    def __init__(self, encryption_key):
        self.fernet = Fernet(encryption_key)
        self.file_path = 'scraped_data.enc.gz'

    async def save(self, data):
        encrypted_data = self.fernet.encrypt(json.dumps(data).encode())
        compressed_data = gzip.compress(encrypted_data)
        with open(self.file_path, 'ab') as f:
            f.write(compressed_data + b'\n')

    async def load(self):
        if not os.path.exists(self.file_path):
            return []

        with open(self.file_path, 'rb') as f:
            compressed_data = f.read().split(b'\n')
        
        decrypted_data = []
        for data in compressed_data:
            if data:
                decompressed = gzip.decompress(data)
                decrypted = self.fernet.decrypt(decompressed).decode()
                decrypted_data.append(json.loads(decrypted))
        
        return decrypted_data

    async def clear(self):
        if os.path.exists(self.file_path):
            os.remove(self.file_path)