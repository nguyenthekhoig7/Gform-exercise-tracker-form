import sqlite3
import pandas as pd

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
            'username': self.username,
            'date': self.date,
            'time': self.time,
            'exercise_order_id': self.exercise_order_id,
            'exercise_name': self.exercise_name,
            'set_id': self.set_id,
            'weight_kg': self.weight_kg,
            'reps_count': self.reps_count,
            'dropdown_weight_kg': self.dropdown_weight_kg,
            'dropdown_reps_count': self.dropdown_reps_count
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
            for set_id, set in enumerate(exercise['sets']):
                self.lift_sets.append(
                    LiftingSet(username, date, time, 
                               exercise['exercise_order_id'], 
                               exercise['exercise_name'], 
                                set_id,
                                set['weight_kg'],
                                set['reps_count'],
                                set['dropdown_weight_kg'],
                                set['dropdown_reps_count']))  
            
    def to_lifting_sets(self):
        return self.lift_sets

    
class ExerciseDB:
    def __init__(self, db_name, exercise_list: list, admin_username: str):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

        # ! BUG: The table is created every time the class is instantiated
        # ! FIX: Check if the table exists before creating it
        self.create_tables(exercise_list=exercise_list, admin_username=admin_username)

    def add_exercise(self, username, exercise_name):
        self.cursor.execute("INSERT INTO exercises (username, exercise_name) VALUES (?, ?)", (username, exercise_name,))
        self.conn.commit()
        print(f"DB Status: Added exercise: {exercise_name}")

    def add_set(self, lifting_set: LiftingSet):
        self.cursor.execute("INSERT INTO lifting_sets (username, date, time, exercise_order_id, exercise_name, set_id, weight_kg, reps_count, dropdown_weight_kg, dropdown_reps_count) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                            (lifting_set.username, lifting_set.date, lifting_set.time, lifting_set.exercise_order_id, lifting_set.exercise_name, lifting_set.set_id, lifting_set.weight_kg, lifting_set.reps_count, lifting_set.dropdown_weight_kg, lifting_set.dropdown_reps_count))
        
        # Commit your changes in the database 
        self.conn.commit() 

        print(f"DB Status: Added record: {lifting_set.__str__()}")

    def add_lifting_sets(self, lifting_sets: list):
        for lifting_set in lifting_sets:
            self.add_set(lifting_set)

    def create_tables(self, exercise_list: list, admin_username: str):

        ''' Create table if not exists
        Add default exercises to the exercises table
        '''
        
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS exercises
             (id INTEGER PRIMARY KEY, username TEXT, exercise_name TEXT)''')
        
        # Insert exercises into the table
        for exercise in exercise_list:
            self.add_exercise(username=admin_username, exercise_name=exercise)

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS lifting_sets
             (id INTEGER PRIMARY KEY, username TEXT, date TEXT, time TEXT, exercise_order_id INTEGER, exercise_name TEXT, set_id INTEGER, weight_kg REAL, reps_count INTEGER, dropdown_weight_kg REAL, dropdown_reps_count INTEGER)''')
        self.conn.commit()

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