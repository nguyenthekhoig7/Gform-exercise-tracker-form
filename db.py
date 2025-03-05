import sqlite3

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
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        
        self.cursor = self.conn.cursor()

        # Create table if not exists
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS exercises
             (id INTEGER PRIMARY KEY, exercise_name TEXT)''')
        
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS lifting_sets
             (id INTEGER PRIMARY KEY, username TEXT, date TEXT, time TEXT, exercise_order_id INTEGER, exercise_name TEXT, set_id INTEGER, weight_kg REAL, reps_count INTEGER, dropdown_weight_kg REAL, dropdown_reps_count INTEGER)''')
        self.conn.commit()

    def add_exercise(self, exercise_name):
        self.cursor.execute("INSERT INTO exercises (exercise_name) VALUES (?)", (exercise_name,))
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
