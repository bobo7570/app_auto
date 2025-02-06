import yaml
from pathlib import Path
from typing import Dict, Any

_config_cache = {}

def load_config(file_name: str = 'config.yaml') -> Dict[str, Any]:
    if file_name in _config_cache:
        return _config_cache[file_name]
    
    config_path = Path(__file__).parent / file_name
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
            _config_cache[file_name] = config
            return config
    except Exception as e:
        logger.error(f"加载配置文件失败: {str(e)}")
        raise 