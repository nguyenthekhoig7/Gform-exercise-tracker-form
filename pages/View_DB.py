# Streamlit file that connects to the database and displays the data in all tables

import streamlit as st
import sqlite3
# Add the parent directory to sys.path
import sys
sys.path.append('..')
from utils import load_config_yaml
import pandas as pd


config = load_config_yaml('config.yaml')
db_name = config['db_name']
admin_username = config['admin_username']

# Initialize/Connect the existed the database
conn = sqlite3.connect(db_name)
cursor = conn.cursor()

st.set_page_config(page_title='View Lifting Data')
st.title('View Lifting Data')

# Input username to view all the data
username = st.text_input('Enter your username')


if username:
    if not username == admin_username:
        st.write('You are not authorized to view the data')
    else:
        # Fetch all table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

        all_table_names = cursor.fetchall()
        all_table_names = [table[0] for table in all_table_names]
        # st.markdown("**All table names in the database:**")
        # st.text(all_table_names)

        # Display all the data in the database
        st.markdown("**Database data**")
        for table in all_table_names:
            cursor.execute(f"SELECT * FROM {table}")
            rows = cursor.fetchall()
            
            columns = [description[0] for description in cursor.description]
            data_with_columns = pd.DataFrame(rows, columns = columns)

            st.markdown(f"Table: **{table}**")
            _, col = st.columns([1, 19])
            with col:   
                st.dataframe(data_with_columns)


