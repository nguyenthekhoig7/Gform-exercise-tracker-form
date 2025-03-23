# config.py
from typing import Dict
import streamlit as st

def load_st_config() -> Dict:
    config = {}

    # Load config with all keys available in .streamlit/secrets.toml
    for key in ['db_name', 'admin_username', 'exercise_list', 'exercise_count', 'set_count', 'primary_muscle_groups', 'secondary_muscle_groups', 'unknown_exercise',
                'exercise_count', 'set_count']:
        config[key] = st.secrets[key]

    return config

config = load_st_config()
PRIM_MUSCLE_GROUPS = config['primary_muscle_groups']
SEC_MUSCLE_GROUPS = config['secondary_muscle_groups']
EXERCISE_COUNT = config['exercise_count']
SET_COUNT = config['set_count']
EXERCISE_LIST = config['exercise_list']
DB_NAME = config['db_name']
ADMIN_USERNAME = config['admin_username']

UNKNOWN_EXERCISE = config['unknown_exercise']

NUM_EXERCISES = config['exercise_count']
NUM_SETS = config['set_count']