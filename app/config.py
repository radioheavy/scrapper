import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    def __init__(self):
        self.config_items = {
            'captcha_api_key': os.getenv('CAPTCHA_API_KEY'),
            'encryption_key': os.getenv('ENCRYPTION_KEY'),
            'max_retries': int(os.getenv('MAX_RETRIES', 5)),
            'min_delay': float(os.getenv('MIN_DELAY', 0.1)),
            'max_delay': float(os.getenv('MAX_DELAY', 1)),
            'target_urls': os.getenv('TARGET_URLS', '').split(','),
            'tor_port': int(os.getenv('TOR_PORT', 9050)),
            'tor_control_port': int(os.getenv('TOR_CONTROL_PORT', 9051)),
            'use_js_rendering': os.getenv('USE_JS_RENDERING', 'True').lower() == 'true',
            'max_concurrent_requests': int(os.getenv('MAX_CONCURRENT_REQUESTS', 50)),
            'user_agent_rotation_frequency': int(os.getenv('USER_AGENT_ROTATION_FREQUENCY', 1)),
            'tor_probability': float(os.getenv('TOR_PROBABILITY', 0.5)),
            'link_follow_probability': float(os.getenv('LINK_FOLLOW_PROBABILITY', 0.8)),
            'max_depth': int(os.getenv('MAX_DEPTH', 5)),
            'respect_robots_txt': os.getenv('RESPECT_ROBOTS_TXT', 'False').lower() == 'true',
            'proxy_rotation_interval': int(os.getenv('PROXY_ROTATION_INTERVAL', 30)),
            'use_stealth_mode': os.getenv('USE_STEALTH_MODE', 'True').lower() == 'true',
            'use_proxy_rotation': os.getenv('USE_PROXY_ROTATION', 'True').lower() == 'true',
            'use_distributed_scraping': os.getenv('USE_DISTRIBUTED_SCRAPING', 'False').lower() == 'true',
            'redis_url': os.getenv('REDIS_URL', 'redis://localhost'),
            'num_workers': int(os.getenv('NUM_WORKERS', 4)),
            'use_advanced_fingerprint_evasion': os.getenv('USE_ADVANCED_FINGERPRINT_EVASION', 'True').lower() == 'true',
            'use_ai_behavior_simulation': os.getenv('USE_AI_BEHAVIOR_SIMULATION', 'True').lower() == 'true',
            'use_ml_proxy_rotation': os.getenv('USE_ML_PROXY_ROTATION', 'True').lower() == 'true',
            'captcha_model_path': os.getenv('CAPTCHA_MODEL_PATH', 'path/to/your/model.h5'),
            'use_content_analysis': os.getenv('USE_CONTENT_ANALYSIS', 'True').lower() == 'true',
        }

    def __getattr__(self, name):
        return self.config_items.get(name)

    def __setattr__(self, name, value):
        if name == 'config_items':
            super().__setattr__(name, value)
        else:
            self.config_items[name] = value

    def to_dict(self):
        return self.config_items

    def update_from_dict(self, new_config):
        for key, value in new_config.items():
            if key in self.config_items:
                self.config_items[key] = value