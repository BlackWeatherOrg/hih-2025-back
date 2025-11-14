"""
Пакет конфигураций приложения, конфигурации переопределяются загрузкой параметров из локального файла.
"""
from config._base import *
from config._custom import *
from internal.core.settings.loaders import local


local.load_config(globals(), filename=f'{APP_DIR}/config/local.yaml')
