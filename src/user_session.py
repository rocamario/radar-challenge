import json
import os


class UserSession:
    def __init__(self, user_id, directory='data'):
        self.user_id = user_id
        self.directory = directory
        self.data = None

        self.timestamp = None
        self.device_type = None
        self.is_touch_capable = None
        self.browser = None
        self.browser_version = None
        self.os = None
        self.os_version = None
        self.device = None
        self.device_brand = None
        self.device_model = None
        self.user_agent_string = None
        self.language_code = None
        self.language = None
        self.language_locality = None
        self.dimensions = None
        self.view_area = None
        self.screen_dimensions = None
        self.screen_area = None
        self.view_ratio = None
        self.height = None
        self.width = None
        self.screen_height = None
        self.screen_width = None
        self.browser_vendor = None
        self.browser_language = None
        self.ad_blocker = None
        self.network_speed = None
        self.platform = None
        self.save_data = None
        self.screen_orientation = None
        self.battery_level = None
        self.battery_charging = None
        self.day_of_week = None
        self.month = None
        self.day_of_month = None
        self.hour = None
        self.season = None
        self.is_holiday = None
        self.holiday_name = None
        self.referer_url = None
        self.referer_domain = None
        self.product_id = None
        self.store_id = None
        self.product_tag = None
        self.utm_source = None
        self.utm_medium = None
        self.utm_campaign = None
        self.utm_content = None
        self.utm_term = None
        self.continent = None
        self.country = None
        self.region = None
        self.city = None
        self.latitude = None
        self.longitude = None
        self.is_eu = None
        self.postal = None
        self.is_capital = None
        self.asn = None
        self.isp = None
        self.currency = None
        self.currency_rate = None
        self.elevation = None
        self.temperature = None
        self.humidity = None
        self.apparent_temperature = None
        self.is_day = None
        self.precipitation = None
        self.weather_code = None
        self.timezone = None

    def load(self):
        path = f"{self.directory}/{self.user_id}.json"
        if not os.path.exists(path):
            print(f"[ERROR] File not found: {path}")
            return

        try:
            with open(path) as f:
                data = json.load(f)
        except Exception as e:
            print(f"[ERROR] Could not load JSON from {path}: {e}")
            return

        self.data = data
        self.timestamp = data.get('timestamp')

        try:
            parameters = json.loads(data.get('parameters', '{}'))
        except json.JSONDecodeError as e:
            print(f"[ERROR] Invalid 'parameters' in {path}: {e}")
            parameters = {}

        for k, v in parameters.items():
            setattr(self, k, v)

        # For debugging: print if something important is missing
        if not hasattr(self, 'country'):
            print(f"[WARNING] Missing 'country' for session {self.user_id}")


    def __str__(self):
        s = f"USER SESSION {self.user_id}\n"
        s += f"Time: {self.timestamp}\n"
        param_dict = json.loads(self.data['parameters'])
        for k in param_dict:
            formatted_k = k.replace("_", " ")
            formatted_k = " ".join([w[0].upper() + w[1:] for w in formatted_k.split()])
            s += f"{formatted_k} : {param_dict[k]}\n"
        return s
