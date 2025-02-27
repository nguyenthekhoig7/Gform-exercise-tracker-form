import yaml
from typing import Dict

def load_config_yaml(config_path: str) -> Dict:
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    return config