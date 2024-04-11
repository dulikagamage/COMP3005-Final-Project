from db_conn import db
from datetime import datetime


class Admin:

    @staticmethod
    def signIn(email, password):
        try:
            conn = db.get_connection()
            cur = conn.cursor()
            query = f'''SELECT * FROM adminStaff WHERE email = %s AND password = %s;'''
            cur.execute(query, (email, password))
            admin = cur.fetchone()
            if admin:
                print("Admin sign in successful")
                return admin[0]
            else:
                return None
        except Exception as error:
            print(error)

    @staticmethod
    def doesClassExist(class_id):
        try:
            conn = db.get_connection()
            cur = conn.cursor()
            cur.execute(f'''SELECT * FROM class WHERE class_id = %s;''', (class_id, ))
            c = cur.fetchone()
            return bool(c)
        except Exception as e:
            print(e)

    @staticmethod
    def doesRoomExist(room_id):
        try:
            conn = db.get_connection()
            cur = conn.cursor()
            cur.execute(f'''SELECT * FROM rooms WHERE room_id = %s''', (room_id,))
            result = cur.fetchone()
            return bool(result)
        except Exception as e:
            print(e)

    @staticmethod
    def doesTrainerExist(trainer_id):
        try:
            conn = db.get_connection()
            cur = conn.cursor()
            cur.execute(f'''SELECT * FROM trainer WHERE trainer_id = %s''', (trainer_id,))
            result = cur.fetchone()
            return bool(result)
        except Exception as e:
            print(e)
            
    @staticmethod
    def deleteRoomBooking(room_booking_id):
        try:
            conn = db.get_connection()
            cur = conn.cursor()
            cur.execute(f'''DELETE FROM roomBooking WHERE room_booking_id = %s RETURNING class_id''', (room_booking_id, ))
            conn.commit()
            c_id = cur.fetchone()[0]
            cur.execute(f'''UPDATE class SET has_room_booking = False, room_id = 0 WHERE class_id = %s''', (c_id, ))
            conn.commit()
        except Exception as e:
            print(e)

    @staticmethod
    def createClass(class_name, trainer_id, room_id, date, time, is_private, has_room_booking = False):
        try:
            if not Admin.doesRoomExist(room_id) or not Admin.doesTrainerExist(trainer_id):
                print("Room ID / Trainer ID invalid")
                return None
            conn = db.get_connection()
            cur = conn.cursor()
            query = f'''INSERT INTO class (class_name, trainer_id, room_id, date, time, is_private)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING class_id;'''
            cur.execute(query,
                        (class_name, trainer_id, room_id, date, time, is_private))
            conn.commit()
            c_id = cur.fetchone()[0]

            print(f"\nClass {c_id} created")
            return c_id
        except Exception as e:
            print(e)

    @staticmethod
    def deleteClass(class_id):
        try:
            conn = db.get_connection()
            cur = conn.cursor()
            cur.execute(f'''DELETE FROM roomBooking WHERE class_id = %s;''', (class_id,))
            cur.execute( f'''DELETE FROM classRegistration WHERE class_id = %s;''', 
                        (class_id,))
            cur.execute(f'''DELETE FROM class WHERE class_id = %s;''', (class_id,))
            conn.commit()

            print(
                f"Deleted class: {class_id} and related room booking and class registrations"
            )

        except Exception as e:
            print(e)

    @staticmethod
    def updateClass(class_id, field, new_val):
        try:
            if not Admin.doesClassExist(class_id):
                raise Exception(f"Class {class_id} does not exist")

            conn = db.get_connection()
            cur = conn.cursor()

            if field == "name":
                field = "class_name"
            elif field == "trainer":
                field = "trainer_id"
            elif field == "room":
                field = "room_id"
            elif field == "privacy":
                field = "is_private"
            else:
                raise Exception(f"Field {field} is not valid")

            cur.execute(f'''UPDATE class SET {field} = %s WHERE class_id = %s''', (new_val, class_id))
            conn.commit()

            print("Class updated successfully")
        except Exception as e:
            print(e)

    @staticmethod
    def displayAllClasses(has_room_booking):
        try:
            conn = db.get_connection()
            cur = conn.cursor()
            cur.execute(f'''SELECT * FROM class WHERE has_room_booking = %s;''', (has_room_booking,))
            result = cur.fetchall()

            print("All classes with valid room bookings:") if has_room_booking else print("All classes with no room booking:")
            for c in result:
                print(f"Class ID {c[0]}")
                print(f"Class Name: {c[1]}, with ID: {c[0]}\nClass Room: {c[3]}\n"
                f"Class Date and Time: {c[4]} at {c[5]}\n"
                f"Class Privacy: {c[6]}\n")
            return result
        except Exception as e:
            print(e)

    @staticmethod
    def doesClassHaveRoom(class_id):
        try:
            conn = db.get_connection()
            cur = conn.cursor()
            cur.execute(f'''SELECT has_room_booking FROM class WHERE class_id = %s''', ([class_id]))
            result = cur.fetchone()
            return result[0]
        except Exception as e:
            print(e)


    @staticmethod
    def findAvailableRooms(class_date, class_time, is_private):
        try:
            conn = db.get_connection()
            cur = conn.cursor()
            rooms = Admin.getPrivacyRooms(is_private)
            free_rooms = []
            if rooms:
                for room in rooms:
                    if Admin.checkRoomAvailability(room[0], class_date, class_time):
                        free_rooms.append(room[0])
            if len(free_rooms) == 0:
                print(f"No empty rooms for {class_date}, {class_time}")
            return free_rooms    
        except Exception as e:
            print(e)

    @staticmethod
    def getClassDateTime(c_id):
        try:
            conn = db.get_connection()
            cur = conn.cursor()
            cur.execute('''SELECT date, time FROM class WHERE class_id = %s;''', (c_id, ))
            result = cur.fetchone()
            return result
        except Exception as e:
            print(e)

    @staticmethod
    def printAvailableRooms(free_rooms):
        if len(free_rooms) == 0:
            raise Exception("All rooms are booked for this time")
        print("All free rooms:")
        for room in free_rooms:
            print(f"Room ID: {room}")

    @staticmethod
    def displayBookingsByPrivacy(privacy):
        try:
            conn = db.get_connection()
            cur = conn.cursor()

            query = f'''SELECT *
                        FROM roomBooking AS t1
                        LEFT JOIN class AS t2
                        ON t1.class_id = t2.class_id
                        WHERE t2.is_private = %s;'''

            cur.execute(query, (privacy,))
            result = cur.fetchall()
            if not result:
                if privacy: 
                    print("No private bookings")
                else:
                    print("No public bookings")
                return None

            for booking in result:
                print("-----------------------------")
                print(f"\nRoom Booking ID: {booking[0]}\nRoom ID: {booking[1]}")
                print(f"Class Name {booking[4]}, with ID: {booking[2]} ")
                print(f"Trainer: {booking[5]}")
                print(f"On date: {booking[7]}\nBooked for 1h starting: {booking[8]}")

            return True

        except Exception as e:
            print(e)

    @staticmethod
    def createRoomBooking(room_id, class_id):
        try:
            conn = db.get_connection()
            cur = conn.cursor()
            if (not Admin.doesClassExist(class_id)):  #class does not exist
                print(f"Class with id {class_id} does not exist")
                return
            query = f'''INSERT INTO roomBooking (room_id, class_id)
                                VALUES (%s, %s) 
                                RETURNING room_booking_id;'''
            cur.execute(query, (room_id, class_id))
            conn.commit()
            new_room_booking_id = cur.fetchone()[0]
            cur.execute(f'''UPDATE class SET has_room_booking = TRUE WHERE class_id = %s''', ([class_id]))
            conn.commit()
            print(f"Created a new room booking, id = {new_room_booking_id}")
            return new_room_booking_id
        except Exception as error:
            print(error)

    @staticmethod
    def displayAllRoomBookings():
        Admin.displayBookingsByPrivacy(True)
        Admin.displayBookingsByPrivacy(False)

    @staticmethod
    def updateRoomBooking(room_booking_id, new_room_id):
        try:
            conn = db.get_connection()
            cur = conn.cursor()
            cur.execute( f'''UPDATE roomBooking SET room_id = %s WHERE room_booking_id = %s;''', (new_room_id, room_booking_id))
            conn.commit()
            cur.execute('''SELECT class_id FROM roomBooking WHERE room_booking_id = %s''', (room_booking_id, ))
            result = cur.fetchone()
            cur.execute( f'''UPDATE class SET room_id = %s WHERE class_id = %s''', (new_room_id, result[0]))
            conn.commit()
        except Exception as e:
            print(e)

    @staticmethod
    def getClassDateTimeFromRoomBooking(room_booking_id):
        try:
            conn = db.get_connection()
            cur = conn.cursor()

            q = '''SELECT c.date, c.time FROM roomBooking rb
                    LEFT JOIN class c
                    ON rb.class_id = c.class_id
                    WHERE rb.room_booking_id = %s'''
            cur.execute(q, ([room_booking_id]))
            result = cur.fetchone()
            date = result[0]
            time = result[1]
            return date, time
        except Exception as e:
            print(e)

    @staticmethod
    def doesRoomBookingExist(room_booking_id):
        try:
            conn = db.get_connection()
            cur = conn.cursor()
            cur.execute(f'''SELECT * FROM roomBooking WHERE room_booking_id = %s''', ([room_booking_id]))
            result = cur.fetchone()
            return bool(result)
        except Exception as e:
            print(e)

    @staticmethod
    def doesEquipmentExist(equip_id):
        try:
            conn = db.get_connection()
            cur = conn.cursor()
            cur.execute(f'''SELECT * FROM equipment WHERE equipment_id = %s''', ([equip_id]))
            result = cur.fetchone()
            return bool(result)
        except Exception as e:
            print(e)

    @staticmethod
    def displayAllEquipment():
        try:
            conn = db.get_connection()
            cur = conn.cursor()
            query = f'''SELECT * FROM equipment;'''
            cur.execute(query)
            equipments = cur.fetchall()
            if equipments:
                for eq in equipments:
                    print(f"\nEquipemnt Name: {eq[1]}, with ID: {eq[0]}\nLast Maintained: {eq[2]}")
        except Exception as error:
            print(error)

    @staticmethod
    def maintainEquipment(equipment_id, date):
        try:
            conn = db.get_connection()
            cur = conn.cursor()
            cur.execute(f'''UPDATE equipment SET maintenance_date = %s WHERE equipment_id = %s;''', (date, equipment_id))
            conn.commit()
        except Exception as error:
            print(error)

    @staticmethod
    def updateBills():
        try:
            conn = db.get_connection()
            cur = conn.cursor()
            cur.execute("SELECT registration_id, class_id, user_id FROM classRegistration")
            registration_class_ids = cur.fetchall()

            for registration_id, class_id, user_id in registration_class_ids:
                # Check if a payment exists for the registration ID
                cur.execute("SELECT payment_id FROM payment WHERE registration_id = %s", (registration_id,))
                payment_exists = cur.fetchone()

                # If payment doesn't exist, calculate amount based on whether the class is private or not
                if not payment_exists:
                    cur.execute("SELECT is_private FROM class WHERE class_id = %s", (class_id,))
                    is_private = cur.fetchone()[0]

                    amount = 40 if is_private else 20 
                    cur.execute("INSERT INTO payment (user_id, registration_id, amount, is_payed) VALUES (%s, %s, %s, %s)",
                                (user_id, registration_id, amount, False))

            conn.commit()
        except Exception as e:
            print(e)

    @staticmethod
    def checkRoomAvailability(room_id, date, time):
        try:
            conn = db.get_connection()
            cur = conn.cursor()
            query = '''
                        SELECT COUNT(*) 
                        FROM class AS c
                        INNER JOIN roomBooking AS rb ON c.class_id = rb.class_id 
                        WHERE rb.room_id = %s 
                        AND c.date = %s 
                        AND c.time = %s
                    '''
            cur.execute(query, (room_id, date, time))
            result = cur.fetchone()
            if result:
                return result[0] == 0
        except Exception as error:
            print(error)

    @staticmethod
    def getPrivacyRooms(is_priv):
        try:
            conn = db.get_connection()
            cur = conn.cursor()
            cur.execute( f'''SELECT * FROM rooms WHERE is_private=%s;''', (is_priv, ))
            priv_rooms = cur.fetchall()
            return priv_rooms if priv_rooms else None
        except Exception as error:
            print(error)
