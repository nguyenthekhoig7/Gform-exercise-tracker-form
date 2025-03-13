import yaml
from typing import Dict

# Deprecated, moved config to .streamlit/secrets.toml
# def load_config_yaml(config_path: str) -> Dict:
#     with open(config_path, 'r') as f:
#         config = yaml.safe_load(f)
#     return config

def load_st_config(streamlit: object) -> Dict:
    config = {}

    # Load config with all keys available in .streamlit/secrets.toml
    for key in ['db_name', 'admin_username', 'exercise_list', 'exercise_count', 'set_count', 'primary_muscle_groups', 'secondary_muscle_groups']:
        config[key] = streamlit.secrets[key]

    return config

def filter_exercises_by_group(exercise_list: list, muscle_group_1: str, muscle_group_2: str):
    '''
    Filter exercised that belong to a group, defined by the [{muscle_group}]
    string at the beginning of an exercise's name.
    '''
    filtered_exercises = [exercise for exercise in exercise_list \
                          if exercise.startswith(f"[{muscle_group_1}]") \
                            or exercise.startswith(f"[{muscle_group_2}]") ]
    return filtered_exercises
