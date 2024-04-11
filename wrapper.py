import sys
from datetime import datetime
from trainers import Trainer
from user import User
from admin import Admin
class Wrapper():

    @staticmethod
    def userUpdateUserInfo(u_id):
        while True:
            try:    
                if not User.doesUserExist(u_id):
                    raise Exception(f"User with id {u_id} does not exist")

                field = input("What field do you want to update (name, email, password, weight, height, goal)?: ")
                new_val = input(f"New value for {field}: ")

                User.updateUserInfo(u_id, field, new_val)
                break
            except Exception as e:
                print(e)
                print("Invalid input try again")

    @staticmethod
    def userPrintUserDashboard(u_id):
        while True:
            try:    
                if not User.doesUserExist(u_id):
                    print(f"User with id {u_id} does not exist")
                    return

                User.printUserDashBoard(u_id)
                break
            except Exception as e:
                print(e)
                print("Invalid input try again")

    @staticmethod
    def userRegisterPublicClass(u_id):
        while True:
            try:
                if not Admin.displayBookingsByPrivacy(False):
                    print("Choose a different option.")
                    break
                if not User.doesUserExist(u_id):
                    raise Exception(f"User with id {u_id} does not exist")

                c_id = int(input("\nEnter the class ID you want to register: "))
                if not Admin.doesClassExist(c_id):
                    raise Exception(f"Class with id {c_id} does not exist")

                User.registerPublicClass(u_id, c_id)
                print(f"Successfully registered in class {c_id}")
                break
            except Exception as e:
                print(e)

    @staticmethod
    def userCancelPublicClass(u_id):
        while True:
            try:
                if not Admin.displayBookingsByPrivacy(False):
                    print("Choose a different option.")
                    break
                if not User.doesUserExist(u_id):
                    raise Exception(f"User with id {u_id} does not exist")

                c_id = int(input("\nEnter the public class ID you want to cancel registration for: "))
                if not Admin.doesClassExist(c_id):
                    raise Exception(f"Class with id {c_id} does not exist")

                User.cancelPublicClass(c_id)
                break
            except Exception as e:
                print(e)


    @staticmethod
    def userPersonalTraining(u_id):
        while True:
            try:    
                if not User.doesUserExist(u_id):
                    raise Exception(f"User with id {u_id} does not exist")
                trainers= Trainer.getAllTrainers()
                if trainers:
                    print("All Trainers: ")
                    for trainer in trainers:
                        Trainer.printTrainer(trainer[0])
                t_id = int(input("\nEnter the trainer ID: "))
                s_time = input("Enter when you want to start (must be on the hour) (HH:MM:SS): ")
                date = input("Enter what date (yyyy-mm-dd): ")

                s_time = datetime.strptime(s_time, "%H:%M:%S").time()
                date = datetime.strptime(date, "%Y-%m-%d").date()

                User.personalTraining(u_id, t_id, s_time, date)
                break
            except Exception as e:
                print(e)
                print("Invalid input try again")

    @staticmethod
    def userReschedulePrivateClass(u_id):
        while True:
            try:
                if not User.doesUserExist(u_id):
                    raise Exception(f"User with id {u_id} does not exist")
                if not User.findUserPrivateTraining(u_id):
                    print("No private classes.")

                c_id = int(input("\nEnter the private class ID you want to reschedule: "))

                if not Admin.doesClassExist(c_id):
                    raise Exception(f"Class with id {c_id} does not exist")

                trainers= Trainer.getAllTrainers()
                if trainers:
                    print("All Trainers: ")
                    for trainer in trainers:
                        Trainer.printTrainer(trainer[0])
                t_id = int(input("\nEnter the trainer you want to reschedule with: "))
                if not Admin.doesTrainerExist(t_id):
                    raise Exception(f"Trainer {t_id} does not exist")

                s_time = input("Enter when you want to start (must be on the hour) (HH:MM:SS): ")
                date = input("Enter what date (yyyy-mm-dd): ")

                s_time = datetime.strptime(s_time, "%H:%M:%S").time()
                date = datetime.strptime(date, "%Y-%m-%d").date()

                User.reschedulePersonalTraining(c_id,t_id,date,s_time)
                break
            except Exception as e:
                print(e)

    @staticmethod
    def userCancelPrivateTraining(u_id):
        while True:
            try:
                if not User.findUserPrivateTraining(u_id):
                    return
                c_id = int(input("Pick a class ID to cancel: "))
                if not Admin.doesClassExist(c_id): #also check if theuser is registered in the class
                    raise Exception(f"Class {c_id} does not exist!")
                User.cancelPersonalTraining(c_id)
                break
            except Exception as e:
                print(e)

    @staticmethod
    def userManagePayment(u_id):
        while True:
            try:
                if not User.outstandingPayments(u_id):
                    return
                usr_in = input("Would you like to make a payment?(Y/N): ")
                if usr_in == "Y" :
                    pay_id = input("Enter the Payment ID: ")
                    User.makePayment(u_id, pay_id)
                elif usr_in =="N":
                    break
                else:
                    print("Input was invalid, try again.")
            except Exception as e:
                print(e)

    @staticmethod
    def trainerSetAvailability(t_id):
        while True:
            try:    
                if not Admin.doesTrainerExist(t_id):
                    raise Exception(f"Trainer with id {t_id} does not exist")

                s_time = input("Enter your start time (HH:MM:SS):")
                e_time = input("Enter your end time (HH:MM:SS):")

                s_time = datetime.strptime(s_time, "%H:%M:%S").time()
                e_time = datetime.strptime(e_time, "%H:%M:%S").time()
                Trainer.setAvailability(t_id, s_time, e_time)
                print("Warning: any classes you have booked will remain")
                print("Any new classes will be restricted to your updated available time")
                break
            except Exception as e:
                print(e)
                print("Invalid input try again")

    @staticmethod
    def trainerViewUserInformation(t_id):
        while True:
            try:    
                fname = input("Enter the first name: ")
                lname = input("Enter the last name: ")
                User.getUserDash(fname, lname)
                break
            except Exception as e:
                print(e)
                print("Invalid input try again")

    @staticmethod
    def adminCreateClassPublic():
        while True:
            try:
                trainers= Trainer.getAllTrainers()
                if trainers:
                    print("All Trainers: ")
                    for trainer in trainers:
                        Trainer.printTrainer(trainer[0])
                t_id = int(input("Enter a trainer to book (ID): "))
                if not Admin.doesTrainerExist(t_id):
                    raise Exception(f"Trainer {t_id} does not exist")
                date = input("Enter a date (yyyy-mm-dd): ")
                time = input("Enter a time (hh:mm:ss): ")
                date = datetime.strptime(date, "%Y-%m-%d").date()
                time = datetime.strptime(time, "%H:%M:%S").time()
                if Trainer.checkBooked(t_id, date, time):
                    raise Exception(f"Trainer {t_id} is booked on {date}, {time}")
                if not Trainer.checkAvailability(t_id, time):
                    raise Exception("Trainer is not available")

                free_rooms = Admin.findAvailableRooms(date, time, False)
                Admin.printAvailableRooms(free_rooms)
                if len(free_rooms) == 0:
                    break
                r_id = int(input("Choose a room to book (ID): "))
                if not Admin.doesRoomExist(r_id):
                    raise Exception(f"Room {r_id} does not exist")

                class_name = input("Enter the class name: ")
                c_id = Admin.createClass(class_name, t_id, r_id, date, time, False) #default is_private to False since its a public class
                Admin.createRoomBooking(r_id, c_id)
                break
            except Exception as e:
                print(e)

    @staticmethod
    def adminShowAllPublicClasses():
        Admin.displayBookingsByPrivacy(False)

    @staticmethod
    def adminCreateRoomBooking():
        while True:
            try:
                r = Admin.displayAllClasses(False)
                if len(r) == 0:
                    print("There are no classes with empty room bookings")
                    break

                c_id = int(input("Choose a class ID:"))
                if not Admin.doesClassExist(c_id):
                    raise Exception(f"Class {c_id} does not exist")

                date, time = Admin.getClassDateTime(c_id)
                free_rooms = Admin.findAvailableRooms(date, time, False)
                Admin.printAvailableRooms(free_rooms)
                if len(free_rooms) == 0:
                    break

                r_id = int(input("Enter a room to book (ID): "))
                if not Admin.doesRoomExist(r_id):
                    raise Exception(f"Room {r_id} does not exist")

                Admin.createRoomBooking(r_id, c_id)
                break
            except Exception as e:
                print(e)

    @staticmethod
    def adminUpdateRoomBooking():
        while True:
            try:
                Admin.displayBookingsByPrivacy(False) #only let admin change public classes
                #maybe check if the booking is a private booking
                rb_id = int(input("Choose a room booking ID: "))
                if not Admin.doesRoomBookingExist(rb_id):
                    raise Exception(f"Room booking {rb_id} does not exist")
                # check if rb_id is valid

                date, time = Admin.getClassDateTimeFromRoomBooking(rb_id)
                free_rooms = Admin.findAvailableRooms(date, time, False)

                Admin.printAvailableRooms(free_rooms)
                if len(free_rooms) == 0:
                    break

                r_id = int(input("Choose a room id: "))
                if not Admin.doesRoomExist(r_id):
                    raise Exception(f"Room {r_id} does not exist")

                Admin.updateRoomBooking(rb_id, r_id)
                break
            except Exception as e:
                print(e)

    @staticmethod
    def adminDeleteRoomBooking():
        while True:
            try:
                if not Admin.displayBookingsByPrivacy(False):
                    break
                rb_id = int(input("Choose a room booking ID: "))
                if not Admin.doesRoomBookingExist(rb_id):
                    raise Exception(f"Room booking {rb_id} does not exist")
                # check if rb_id is valid

                Admin.deleteRoomBooking(rb_id)
                break
            except Exception as e:
                print(e)

    @staticmethod
    def adminMaintainEquipment():
        while True:
            try:
                Admin.displayAllEquipment()
                update = input("Would you like to update any of the maintence dates?(Y/N): ")
                if update == "Y":
                    eq_id = input("Enter the Equipment ID: ")
                    date = input("Enter the new date: (yyyy-mm-dd): ")
                    date = datetime.strptime(date, "%Y-%m-%d")
                    if Admin.doesEquipmentExist(eq_id):
                        Admin.maintainEquipment(eq_id, date)
                    else:
                        print("Equipment ID you entered does not exist")
                elif update == "N":
                    break
                else:
                    print("Invalid input, try again.")
            except Exception as e:
                print(e)

    @staticmethod
    def adminUpdateBillings():
        while True:
            try:
                Admin.updateBills()
                print("Bills updated and sent")
                break
            except Exception as e:
                print(e)

