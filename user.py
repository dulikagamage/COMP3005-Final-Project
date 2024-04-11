from trainers import Trainer
from admin import Admin
from db_conn import db
from datetime import datetime

class User:
    @staticmethod
    def doesUserExist(user_id):
        try:
            conn = db.get_connection()
            cur = conn.cursor()
            cur.execute(f'''SELECT * FROM users WHERE user_id = %s;''', (user_id,))
            user = cur.fetchone()
            return bool(user)
        except Exception as e:
            print(e)

  
    @staticmethod
    def registerUser(first_name, last_name, email, password, weight, height, goal):
        try:
            
            conn = db.get_connection()
            cur = conn.cursor()
            query = f''' INSERT INTO users (first_name, last_name, email, password) VALUES (%s, %s, %s, %s)  RETURNING user_id;'''
            cur.execute(query, (first_name, last_name, email, password))
            conn.commit()
            user_id = cur.fetchone()[0]
            cur.execute(f''' INSERT INTO userMetrics (user_id, height, weight) VALUES (%s, %s, %s);''', (user_id, height, weight))
            cur.execute(f''' INSERT INTO goals (user_id, goal_weight) VALUES (%s, %s);''', (user_id, goal))
            conn.commit()
        except Exception as error:
            print(error)
            return None
        
    @staticmethod
    def signIn(email, password):    
        try:
            conn = db.get_connection()
            cur = conn.cursor()
            cur.execute(f'''SELECT * FROM users WHERE email = %s AND password = %s;''', (email, password))
            user = cur.fetchone()
            if user:
                return user[0]  # Return the user_id
            return None
        except Exception as error:
            print(error)

    @staticmethod
    def updateUserInfo(user_id, field, new_val):
        try:
            conn = db.get_connection()
            cur = conn.cursor()

            if field == "name":
                new_first_name, new_last_name = new_val.split()
                cur.execute(f'''UPDATE users SET first_name = %s, last_name = %s WHERE user_id = %s;''', (new_first_name, new_last_name, user_id))
                print("User name updated successfully!")
            elif field == "email":
                cur.execute(f'''UPDATE users SET email = %s WHERE user_id = %s;''', (new_val, user_id))
                print("User email updated successfully!")
            elif field == "password":
                cur.execute(f'''UPDATE users SET password = %s WHERE user_id = %s;''', (new_val, user_id))
                print("User password updated successfully!")
            elif field == "weight":
                cur.execute( f'''UPDATE userMetrics SET weight = %s WHERE user_id = %s;''', (new_val, user_id))
                print("User weight updated successfully!")
            elif field == "height":
                cur.execute(f'''UPDATE userMetrics SET height = %s WHERE user_id = %s;''', (new_val, user_id))
                print("User height updated successfully!")
            elif field == "goal":
                cur.execute(f'''UPDATE goals SET goal_weight = %s WHERE user_id = %s;''', (new_val, user_id))
                print("User goal updated successfully!")
            else:
                print("Not an option. Try again.")
            conn.commit()

        except Exception as error:
            print(error)

    @staticmethod
    def printUserDashBoard(user_id):
        try:

            conn = db.get_connection()
            cur = conn.cursor()
            cur.execute(f'''SELECT * FROM users WHERE user_id = %s;''', (user_id, ))
            user = cur.fetchone()
            if user:
                print(f"\nName: {user[1]} {user[2]}, with ID: {user[0]}\nEmail: {user[3]}\n")
            else:
                print("User not found.")

            cur.execute(f'''SELECT * FROM userMetrics WHERE user_id = %s;''', (user_id, ))
            user_metric = cur.fetchone()

            if user_metric:
                print(f"Health Statistics: \nHeight: {user_metric[1]} cm\nWeight: {user_metric[2]} lbs")
            else:
                print("User metrics not found.")

            cur.execute(f'''SELECT * FROM goals WHERE user_id = %s;''', (user_id, ))
            goal = cur.fetchone()

            if goal:
                print(f"Goal Weight: {goal[1]} lbs")
            else:
                print("User goal not found.")

            routine_query = f'''
                SELECT c.class_id, c.class_name, c.room_id, c.date, c.time
                FROM class c
                INNER JOIN classRegistration cr ON c.class_id = cr.class_id
                WHERE cr.user_id = %s;'''
            cur.execute(routine_query, (user_id, ))
            classes = cur.fetchall()

            if classes:
                print("\nRoutines: ")
                for routines in classes:
                    c_id, name, r_id, date, time = routines
                    print(f"Class Name: {name}, with ID: {c_id}\nRoom: {r_id}\nDate and time: {date} at {time}\n")

        except Exception as error:
            print(error)

    @staticmethod
    def getAllUsers():
        try:
            conn = db.get_connection()
            cur = conn.cursor()
            cur.execute(f'''SELECT user_id, first_name, last_name, email FROM users;''')
            users = cur.fetchall()
            return users
        except Exception as error:
            print(error)

    @staticmethod
    def checkBooked(user_id, date, time):
        try:
            conn = db.get_connection()
            cur = conn.cursor()
            query=f'''SELECT cr.registration_id
            FROM classRegistration cr
            JOIN class c ON cr.class_id = c.class_id
            WHERE cr.user_id = %s
            AND c.date = %s
            AND c.time = %s;'''
            cur.execute(query, (user_id, date, time))
            booked_classes = cur.fetchall()

            return bool(booked_classes)

        except Exception as error:
            print (error)

    @staticmethod
    def personalTraining(user_id, trainer_id, start_time, date):

        start_hour, start_minute, start_sec = start_time.hour, start_time.minute, start_time.second

        if not (start_minute == 0 and start_sec == 0 and start_hour <= 24 and start_hour >= 0):
            print("New time is not valid.")
            return

        try:
            conn = db.get_connection()
            cur = conn.cursor()

            #get and set up the trainer
            trainer = Trainer.getTriainer(trainer_id)
            if trainer:
                trainer_id, first_name, last_name, email, password, t_start, t_end = trainer
                if User.checkBooked(user_id, date, start_time):
                    print("You are already booked at this time.")
                    return

                #check if trainer is already booked
                if not Trainer.checkBooked(trainer_id, date, start_time): #trainer is not booked
                    if not Trainer.checkAvailability(trainer_id, start_time):
                        print("Trainer does not work at that time")
                        return
                        #make a class
                    f_name = str(User.getUserName(user_id))
                    class_name = f"{f_name} Private Lesson with {first_name} {last_name}"

                    #find a room
                    room_id = 0
                    priv_rooms = Admin.getPrivacyRooms(True)
                    if priv_rooms:
                        for room in priv_rooms:
                            if Admin.checkRoomAvailability(room[0], date, start_time)==True:
                                room_id = room[0]
                                break
                        #if no room found
                    if room_id == 0:
                        print("No available private rooms for this date and time.\nPrivate class was not booked successfully.")
                        return
                    class_id = Admin.createClass(class_name, trainer_id, room_id, date, start_time, True, has_room_booking = True)
                    Admin.createRoomBooking(room_id, class_id)
                    cur.execute(f'''INSERT INTO classRegistration (user_id, class_id) VALUES (%s, %s);''', (user_id, class_id))
                    conn.commit()
                    print("Private class booked successfully!")
            else:
                print("Trainer is already booked on that date and time")
        except Exception as error:
            print(error)

    @staticmethod
    def reschedulePersonalTraining(class_id, trainer_id, new_date, new_time):
        #check new time is valid
        new_hour, new_min, new_sec = new_time.hour, new_time.minute, new_time.second
        if not (new_min == 0 and new_sec == 0 and new_hour <= 24 and new_hour >= 0):
            print("New time is not valid.")
            return

        try:
            conn = db.get_connection()
            cur = conn.cursor()
            if not Admin.doesClassExist(class_id):
                print("Class does not exist")
                return
            trainer = Trainer.getTriainer(trainer_id)
            if trainer:
                trainer_id, first_name, last_name, email, password, t_start, t_end = trainer
                cur.execute(f'''SELECT user_id FROM classRegistration WHERE class_id = %s;''', (class_id, ))
                user_id = cur.fetchone()
                if user_id:
                    user_id = user_id[0]
                if User.checkBooked(user_id, new_date, new_time):
                    print("You are already booked at this time.")
                    return

                if new_hour >= t_start.hour and (new_hour + 1) <= t_end.hour:

                    if not Trainer.checkBooked(trainer_id, new_date, new_time):
                        if not Trainer.checkAvailability(trainer_id, new_time):
                            print("Trainer does not work at that time")
                            return
                        cur.execute(f'''SELECT room_id FROM class WHERE class_id = %s;''', (class_id, ))
                        room_id = cur.fetchone()

                        if not Admin.checkRoomAvailability(room_id, new_date, new_time): #if the same room isnt available
                            room_id = 0
                            priv_rooms = Admin.getPrivacyRooms(True)
                            if priv_rooms:
                                for room in priv_rooms:
                                    if Admin.checkRoomAvailability(room[0], new_date, new_time):
                                        room_id = room[0]
                                        break
                            #if no room found
                            if room_id == 0:
                                print("No available private rooms for this date and time.\nPrivate class was not rescheduled successfully.")
                                return

                        cur.execute(f"UPDATE class SET date=%s, time = %s, room_id = %s WHERE class_id = %s;", (new_date, new_time, room_id, class_id))
                        cur.execute(f"UPDATE roomBooking SET room_id = %s WHERE class_id = %s;", (room_id, class_id))
                        conn.commit()
                        print("Class updated sucessfully!")
                    else:
                        print("Trainer is booked at that time")
            
            cur.close()

        except Exception as error:
            print(error)

    @staticmethod
    def cancelPersonalTraining(class_id):
        try:
            conn = db.get_connection()
            cur = conn.cursor()
            if not Admin.doesClassExist(class_id):
                print("Class does not exist")
                return
            cur.execute(f"SELECT registration_id FROM classRegistration WHERE class_id = %s;", (class_id, ))
            reg_id = cur.fetchone()
            #check if they paid
            cur.execute(f"SELECT * FROM payment WHERE registration_id=%s;", (reg_id, ))
            payment = cur.fetchone()
            if payment:
                if payment[4]:
                    print("You have been refunded to your email.")
                cur.execute(f"DELETE FROM payment WHERE registration_id = %s;", (reg_id, ))
                conn.commit()

            Admin.deleteClass(class_id)

            print("Class sucessfully cancelled")

        except Exception as error:
            print(error)

    @staticmethod
    def registerPublicClass(user_id, class_id):
        try:
            conn = db.get_connection()
            cur = conn.cursor()
            if not Admin.doesClassExist(class_id):
                print("Class does not exist")
                return
            cur.execute(f'''SELECT date, time FROM class WHERE class_id = %s;''', (class_id, ))
            d_and_t = cur.fetchall()
            if not User.checkBooked(user_id, d_and_t[0][0], d_and_t[0][1]):
                cur.execute('''INSERT INTO classRegistration (user_id, class_id) VALUES (%s, %s)''', (user_id, class_id))
                conn.commit()
            else:
                print("You are already booked at this time.")
        except Exception as error:
            print(error)

    @staticmethod
    def cancelPublicClass(class_id):
        try:
            conn = db.get_connection()
            cur = conn.cursor()
            if not Admin.doesClassExist(class_id):
                print("Class does not exist")
                return
            cur.execute(f"SELECT registration_id FROM classRegistration WHERE class_id = %s;", (class_id, ))
            reg_id = cur.fetchone()
            #check if they paid
            cur.execute( f"SELECT * FROM payment WHERE registration_id=%s", (reg_id, ))
            payment = cur.fetchone()
            if payment:
                if payment[4]:
                    print("You have been refunded to your email.")
                cur.execute(f"DELETE FROM payment WHERE registration_id = %s;", (reg_id, ))

            cur.execute(f"DELETE FROM classRegistration WHERE class_id = %s;", (class_id, ))
            conn.commit()

            print("Registration was sucessfully cancelled")

        except Exception as error:
            print(error)

    @staticmethod
    def getUserDash(first_name, last_name):
        users = User.getAllUsers()
        if users:
            for user in users:
                if user[1] == first_name and user[2] == last_name:
                    User.printUserDashBoard(user[0])

    @staticmethod
    def getUserName(user_id):
        users = User.getAllUsers()
        if users:
            for user in users:
                if int(user[0]) == int(user_id):
                    return user[1] + " " + user[2]

    @staticmethod
    def outstandingPayments(user_id):
        try:
            conn = db.get_connection()
            cur = conn.cursor()
            cur.execute(f"SELECT * FROM payment WHERE user_id=%s AND is_payed = False", (user_id, ))
            payments = cur.fetchall()
            if payments:
                for payment in payments:
                    print(f"Payement ID: {payment[0]}")
                    print(f"Amount Owed: {payment[3]}\n")
                return True
            else:
                print("No outstanding payments")
                return False
        except Exception as error:
            print(error)

    @staticmethod
    def makePayment(user_id, payment_id):
        try:
            conn = db.get_connection()
            cur = conn.cursor()
            cur.execute(f"SELECT * FROM payment WHERE payment_id=%s AND user_id = %s", (payment_id, user_id))
            pay = cur.fetchone()

            if pay:
                print("The payment was recieved")
                cur.execute(f"UPDATE payment SET is_payed = TRUE WHERE payment_id=%s", (payment_id, ))
                conn.commit()
            else:
                print("No such payment ID")

        except Exception as error:
            print(error)

    @staticmethod
    def findUserPrivateTraining(user_id):
        try:
            conn = db.get_connection()
            cur = conn.cursor()

            q = f'''SELECT cr.class_id, c.class_name
                    FROM classRegistration cr
                    JOIN class c
                    ON cr.class_id = c.class_id
                    WHERE c.is_private = TRUE AND cr.user_id = %s;'''

            cur.execute(q, (user_id, ))
            result = cur.fetchall()

            if result:
                for private_class in result:
                    print(f"Private Class ID: {private_class[0]}")
                    print(f"Private Class Name: {private_class[1]}\n")
            else:
                print("You have no private classes.")
                return False

            return True
        except Exception as e:
            print(e)


