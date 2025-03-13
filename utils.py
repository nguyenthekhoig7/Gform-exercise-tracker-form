import yaml
from typing import Dict

def load_config_yaml(config_path: str) -> Dict:
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
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
