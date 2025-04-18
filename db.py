import sqlite3
import pandas as pd
from typing import Literal
from config import ItemKeys

class LiftingSet:
    #     Each record is a row, with columns: date, time, exercise_name, set_id, weight, reps_count, dropdown_weight_kg, dropdown_reps_count
    def __init__(self, 
                 username,
                 date,
                 time,
                 exercise_order_id,
                 exercise_name,
                 set_id,
                 weight_kg,
                 reps_count,
                 dropdown_weight_kg,
                 dropdown_reps_count):
        self.username = str(username)
        self.date = str(date)
        self.time = str(time)
        self.exercise_order_id = int(exercise_order_id)
        self.exercise_name = str(exercise_name)
        self.set_id = int(set_id)
        self.weight_kg = int(weight_kg)
        self.reps_count = int(reps_count)
        self.dropdown_weight_kg = int(dropdown_weight_kg)
        self.dropdown_reps_count = int(dropdown_reps_count)

    def __dict__(self):
        return {
            ItemKeys.USERNAME: self.username,
            ItemKeys.DATE: self.date,
            ItemKeys.TIME: self.time,
            ItemKeys.EXERCISE_ORDER_ID: self.exercise_order_id,
            ItemKeys.EXERCISE_NAME: self.exercise_name,
            ItemKeys.SET_ID: self.set_id,
            ItemKeys.WEIGHT_KG: self.weight_kg,
            ItemKeys.REPS_COUNT: self.reps_count,
            ItemKeys.DROPDOWN_WEIGHT_KG: self.dropdown_weight_kg,
            ItemKeys.DROPDOWN_REPS_COUNT: self.dropdown_reps_count
        }
    
    def __str__(self):
        return f"Username: {self.username}, Date: {self.date}, Time: {self.time}, Exercise: {self.exercise_name}, Set ID: {self.set_id}, Weight (kg): {self.weight_kg}, reps_count: {self.reps_count}, Dropdown Weight (kg): {self.dropdown_weight_kg}, Dropdown reps_count: {self.dropdown_reps_count}"

class LiftingSetsEachDay:
    # List of LiftingSet objects
    def __init__(self,
                 username,
                 date, 
                 time,
                 exercises: list):
        self.username = username
        self.date = date
        self.time = time
        self.lift_sets = []
        for exercise in exercises:
            if exercise['exercise_name'] is None: continue
            for set_id, set in enumerate(exercise.get(ItemKeys.SETS)):
                self.lift_sets.append(
                    LiftingSet(username, date, time, 
                               exercise.get(ItemKeys.EXERCISE_ORDER_ID), 
                               exercise.get(ItemKeys.EXERCISE_NAME), 
                                set_id,
                                set.get(ItemKeys.WEIGHT_KG),
                                set.get(ItemKeys.REPS_COUNT),
                                set.get(ItemKeys.DROPDOWN_WEIGHT_KG),
                                set.get(ItemKeys.DROPDOWN_REPS_COUNT)))
            
    def to_lifting_sets(self):
        return self.lift_sets
    
class TableModel:
    table_name: str
    sqlite_types: dict

class UserModel(TableModel):
    """
    Manage user information, including
        . username  
        . tier (admin, user)
    """
    table_name = 'users'
    sqlite_types = {
            ItemKeys.USERNAME: 'TEXT',
            ItemKeys.TIER: 'TEXT'
        }

class LiftingSetModel(TableModel):
    """
    Manage lifting set information, including
        . username -> user_id
        . date
        . time
        . exercise_order_id
        . exercise_name -> exercise_id
        . set_id
        . weight_kg
        . reps_count
        . dropdown_weight_kg
    """
    table_name = 'lifting_sets'
    sqlite_types = {
            ItemKeys.USERNAME: 'TEXT',
            ItemKeys.DATE: 'TEXT',
            ItemKeys.TIME: 'TEXT',
            ItemKeys.EXERCISE_ORDER_ID: 'INTEGER',
            ItemKeys.EXERCISE_NAME: 'TEXT',
            ItemKeys.SET_ID: 'INTEGER',
            ItemKeys.WEIGHT_KG: 'REAL',
            ItemKeys.REPS_COUNT: 'INTEGER',
            ItemKeys.DROPDOWN_WEIGHT_KG: 'REAL',
            ItemKeys.DROPDOWN_REPS_COUNT: 'INTEGER'
        }

class ExerciseModel(TableModel):
    """
    Manage exercise information, including
        . username  
        . exercise_name
    """
    table_name = 'exercises'
    sqlite_types = {
            ItemKeys.USERNAME: 'TEXT',
            ItemKeys.EXERCISE_NAME: 'TEXT'
        }

    
class ExerciseDB:

    def __init__(self, db_name, exercise_list: list, admin_username: str):
        self.default_exercises = exercise_list
        self.admin_username = admin_username
        check_same_thread = False # Overcome the error caused by Flask's multithread: sqlite3.ProgrammingError: SQLite objects created in a thread can only be used in that same thread.
        self.conn = sqlite3.connect(db_name, check_same_thread=check_same_thread)
        self.cursor = self.conn.cursor()

        self.user_model = UserModel()
        self.exercise_model = ExerciseModel()
        self.lifting_set_model = LiftingSetModel()
        self.create_tables(exercise_list=self.default_exercises, 
                           admin_username=self.admin_username)

    def add_exercise(self, username, exercise_name):
        self.cursor.execute(
            f"SELECT * FROM exercises WHERE {ItemKeys.USERNAME} = ? AND {ItemKeys.EXERCISE_NAME} = ?", 
            (username, exercise_name,))
        
        if self.cursor.fetchone() is not None:
            # print(f"DB Status: Exercise {exercise_name} already exists for user {username}")
            return False
        else:
            insert_command = f"INSERT INTO exercises ({ItemKeys.USERNAME}, {ItemKeys.EXERCISE_NAME}) VALUES (?, ?)"
            insert_command_with_values = (insert_command, (username, exercise_name,))
            self.cursor.execute(*insert_command_with_values)

            print(f"DB Status: Added exercise: {exercise_name} for user {username}")
            self.conn.commit()  
            return True

    def add_set(self, lifting_set: LiftingSet):
        self.cursor.execute("INSERT INTO lifting_sets ({}, {}, {}, {}, {}, {}, {}, {}, {}, {}) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)".format(
                            ItemKeys.USERNAME, ItemKeys.DATE, ItemKeys.TIME, ItemKeys.EXERCISE_ORDER_ID, ItemKeys.EXERCISE_NAME, ItemKeys.SET_ID, ItemKeys.WEIGHT_KG, ItemKeys.REPS_COUNT, ItemKeys.DROPDOWN_WEIGHT_KG, ItemKeys.DROPDOWN_REPS_COUNT), 
                            (lifting_set.username, lifting_set.date, lifting_set.time, lifting_set.exercise_order_id, lifting_set.exercise_name, lifting_set.set_id, lifting_set.weight_kg, lifting_set.reps_count, lifting_set.dropdown_weight_kg, lifting_set.dropdown_reps_count))
        
        self.conn.commit()

        print(f"DB Status: Added record: {lifting_set.__str__()}")

    def add_lifting_sets(self, lifting_sets: list):
        for lifting_set in lifting_sets:
            self.add_set(lifting_set)

    def create_tables(self, exercise_list: list, admin_username: str):

        ''' Create table if not exists
        Add default exercises to the exercises table
        '''
        print(f"DB Status: Creating tables")
        
        self.create_table(self.user_model)
        self.create_table(self.exercise_model)
        self.create_table(self.lifting_set_model)
        
        # Insert admin user if not exists
        if not self.user_exists(admin_username):
            self.add_user(username=admin_username, tier='admin')
            print(f"DB Status: Added admin user: {admin_username}")

        # Insert default exercises for admin user if not exists
        for exercise in exercise_list:
            self.add_exercise(username=admin_username, exercise_name=exercise)

        self.conn.commit()

    

    def create_table(self, table_model: TableModel):
        ''' Create table if not exists '''
        create_table_comand = f"CREATE TABLE IF NOT EXISTS {table_model.table_name}"
        create_table_comand += " (id INTEGER PRIMARY KEY, {} )".format(', '.join([f"{key} {value}" for key, value in table_model.sqlite_types.items()]))
        # print(f"DB Status: {create_table_comand}")
        self.cursor.execute(create_table_comand)
        self.conn.commit()
        # print(f"DB Status: Created table {table_model.table_name}")

    def get_data(self, table_name, username: str = None):
        if username is not None:
            self.cursor.execute(f"SELECT * FROM {table_name} WHERE username = '{username}'")
        else:
            self.cursor.execute(f"SELECT * FROM {table_name}")
        rows = self.cursor.fetchall()
        columns = [description[0] for description in self.cursor.description]
        return pd.DataFrame(rows, columns = columns)
    
    def get_all_table_name(self):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        all_table_names =  self.cursor.fetchall()
        return [table[0] for table in all_table_names]
    
    def reset_db(self, username: str, db_name : Literal['exercises', 'lifting_sets', 'all']):
        ''' Clear all records from all tables in database '''
        if username != self.admin_username:
            raise ValueError("Only admin can clear the database!")
        
        if db_name == 'all':
            for table in ['exercises', 'lifting_sets']:
                self.cursor.execute(f"DROP TABLE IF EXISTS {table}")
        else:
            self.cursor.execute(f"DROP TABLE IF EXISTS {db_name}")

        self.create_tables(exercise_list=self.default_exercises, admin_username=username)

    def add_user(self, username: str, tier: str):
        ''' Add user to the database if not exists '''
        # Check if user already exists
        self.cursor.execute(f"SELECT * FROM {self.user_model.table_name} WHERE {ItemKeys.USERNAME} = '{username}'")
        if self.cursor.fetchone() is not None:
            print(f"DB Status: User {username} already exists")
            return True
        else:
            self.cursor.execute(f"INSERT INTO {self.user_model.table_name} ({ItemKeys.USERNAME}, {ItemKeys.TIER}) VALUES ('{username}', '{tier}')")
            self.conn.commit()

            self.add_default_exercises(username=username)
            print(f"DB Status: Added user: {username} with tier: {tier} to {self.user_model.table_name} and added default exercises")

            
            # Just for debugging, remove later
            self.cursor.execute(f"SELECT * FROM {self.user_model.table_name}")
            rows = self.cursor.fetchall()
            print(f"DB Status: {self.user_model.table_name} data: \n{rows}")
            return True

    def add_default_exercises(self, username: str):
        ''' Add default exercises to the user '''
        print(f"add_default_exercises: {username}")
        for exercise in self.default_exercises:
            self.add_exercise(username=username, exercise_name=exercise)

        print(f"DB Status: Added default exercises for user {username}: {self.default_exercises}")

        # Just for debugging, remove later
        self.cursor.execute(f"SELECT * FROM exercises WHERE username = '{username}'")
        rows = self.cursor.fetchall()
        print(f"DB Status: exercises data: \n{rows}")

    def get_user_exercise_list(self, username: str):
        ''' Fetch exercise list for a user '''
        self.cursor.execute(f"SELECT exercise_name FROM exercises WHERE username = '{username}'")
        rows = self.cursor.fetchall()
        print(f"DB Status: Fetched exercise list for user {username}: \n{rows}")
        return [row[0] for row in rows]
    
    def user_exists(self, username: str):
        ''' Check if user exists in the database '''
        self.cursor.execute(f"SELECT * FROM {self.user_model.table_name} WHERE {ItemKeys.USERNAME} = '{username}'")
        result = self.cursor.fetchone()  # Fetch the result once

        if result is None:
            return False
        else:
            return len(result) > 0


if __name__ == "__main__":

    # Example usage
    db = ExerciseDB(db_name="exercise.db", exercise_list=["Bench Press", "Squat", "Deadlift"], admin_username="admin")
    db.create_user_table()