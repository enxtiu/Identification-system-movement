import logging.config
import yaml
import os

def setup_logging(default_path='logging_config.yaml', default_level=logging.INFO):
    """Настройка логирования через YAML"""
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    try:
        with open(default_path, 'r') as f:
            config = yaml.safe_load(f.read())
            logging.config.dictConfig(config)
    except Exception as e:
        print(f"Ошибка загрузки конфигурации логов: {e}")
        logging.basicConfig(level=default_level)

setup_logging()

logger = logging.getLogger('my_logger')
logger.info("Инфо")
logger.debug("Дебаг")
logger.error("Ошибка")