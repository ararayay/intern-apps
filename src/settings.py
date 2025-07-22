from integration_utils.its_utils.mute_logger import MuteLogger
from integration_utils.bitrix24.local_settings_class import LocalSettingsClass
from config.settings import *


ilogger = MuteLogger()

NGROK_URL = 'http://localhost:8000'
APP_SETTINGS = LocalSettingsClass(
    portal_domain='b24-jgbdfj.bitrix24.ru',
    app_domain='127.0.0.1:8000',
    app_name='bitrix_app',
    salt=os.getenv('SALT'),
    secret_key=os.getenv('JWT_TOKEN'),
    application_bitrix_client_id=os.getenv('APPLICATION_BITRIX_CLIENT_ID'),
    application_bitrix_client_secret=os.getenv('APPLICATION_BITRIX_CLIENT_SECRET'),
    application_index_path='/',
)