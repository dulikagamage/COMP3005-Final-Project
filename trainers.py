from datetime import datetime, time, timedelta
from db_conn import db
class Trainer:

    @staticmethod     
    def signIn(email, password):
        try:
            conn = db.get_connection()
            cur = conn.cursor()
            cur.execute(f'''SELECT * FROM trainer WHERE email = %s AND password = %s;''', (email, password))
            trainer = cur.fetchone()
            if trainer:
                print("Sign-in successful!")
                return trainer[0]  # Return the trainer_id
            else:
                return None

        except Exception as error:
            print (error)

    @staticmethod
    def setAvailability(trainer_id, start_time, end_time):
        try:
            conn = db.get_connection()
            cur = conn.cursor()
            cur.execute( f'''UPDATE trainer SET start_time = %s, end_time = %s WHERE trainer_id = %s;''', (start_time, end_time, trainer_id))
            conn.commit()
            print("Trainer availability updated successfully!")
        except Exception as error:
            print (error)

    @staticmethod
    def getAllTrainers():
        try:
            conn = db.get_connection()
            cur = conn.cursor()
            cur.execute( f'''SELECT trainer_id, first_name, last_name, email, start_time, end_time FROM trainer;''')
            trainers = cur.fetchall()
            return trainers
        except Exception as error:
            print (error)

    @staticmethod
    def getTriainer(trainer_id):
        try:
            conn = db.get_connection()
            cur = conn.cursor()
            cur.execute(f'''SELECT * FROM trainer WHERE trainer_id = %s;''', (trainer_id,))
            trainer = cur.fetchone()
            return trainer
        except Exception as error:
            print (error)
            return None

    @staticmethod
    def getAvailability( trainer_id):
        try:
            conn = db.get_connection()
            cur = conn.cursor()
            cur.execute(f'''SELECT start_time, end_time FROM trainer WHERE trainer_id = %s;''', (trainer_id,))
            trainer_avail = cur.fetchone()
            return trainer_avail
        except Exception as error:
            print (error)
            return None

    @staticmethod
    def printTrainer(trainer_id):
        try:
            conn = db.get_connection()
            cur = conn.cursor()
            cur.execute(f'''SELECT trainer_id, first_name, last_name, email, start_time, end_time FROM trainer WHERE trainer_id = %s;''', (trainer_id,))
            trainer = cur.fetchone()
            if trainer:
                trainer_id, first_name, last_name, email, start, end = trainer
                print(f"\nTrainer: {first_name} {last_name}, with ID: {trainer_id}\nEmail: {email}\nWorking from {start} to {end} everyday")
            else:
                print("Trainer not found.")
        except Exception as error:
            print (error)

    @staticmethod
    def checkAvailability(trainer_id, time):
        try:
            conn = db.get_connection()
            cur = conn.cursor()
            cur.execute(f'''SELECT start_time, end_time FROM trainer WHERE trainer_id = %s;''', (trainer_id,))
            result = cur.fetchone()

            datetime_time = datetime.combine(datetime.today(), time) + timedelta(hours=1)
            end = datetime_time.time()
            if time >= result[0] and end <= result[1]:
                return True
            return False
        except Exception as e:
            print(e) 

    @staticmethod
    def checkBooked(trainer_id, date, time):
        try:
            conn = db.get_connection()
            cur = conn.cursor()
            cur.execute(f'''SELECT * FROM class WHERE trainer_id = %s AND date = %s AND time = %s;''', (trainer_id, date, time))
            booked_classes = cur.fetchall()
            return ( bool(booked_classes) )
        except Exception as error:
            print (error)

