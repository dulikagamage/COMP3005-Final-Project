import sys
from user import User
from trainers import Trainer
from admin import Admin
from userType import UserType
from wrapper import Wrapper

# keep track of what type of user is logged in
loggedInUser = UserType.UNKNOWN
loggedInUserId = -1

def signInMenu():
    print("--------------------------------------------------------")
    print("Please sign in by choosing one of the following options:")
    print(" (1) Sign in as Member\n (2) Sign in as Trainer\n (3) Sign in as Administrative Staff")
    print("Don't already have an account?:")
    print(" (4) Sign up as a new Member!")
    print("---------------------------------------------------------")

def userMenu():
    print("---------------------------------------------------------")
    print("What would you like to do?")
    print("(1) Manage profile")
    print("(2) Display dashboard")
    print("(3) Register for a public class")
    print("(4) Book a private class")
    print("(5) Cancel a private class")
    print("(6) Cancel a public class")
    print("(7) Reschedule a private class")
    print("(8) Show my payments")
    print("(9) Exit")
    print("---------------------------------------------------------")
    #return # of options to use later
    return 9

def trainerMenu():
    print("---------------------------------------------------------")
    print("What would you like to do?")
    print("(1) Update available times")
    print("(2) View a member profile")
    print("(3) Exit")
    print("---------------------------------------------------------")
    return 3

def adminMenu():
    print("---------------------------------------------------------")
    print("What would you like to do?")
    print("(1) Create a new public class")
    print("(2) Show all public class bookings")
    print("(3) Create a room booking for a class")
    print("(4) Update a room booking")
    print("(5) Delete a room booking")
    print("(6) Maintain equipment")
    print("(7) Send billing to clients")
    print("(8) Exit")
    print("---------------------------------------------------------")
    return 8

#store corresponding menu functions in an array
menu = [userMenu, trainerMenu, adminMenu] 
f1 = [Wrapper.userUpdateUserInfo, Wrapper.userPrintUserDashboard, Wrapper.userRegisterPublicClass,
      Wrapper.userPersonalTraining, Wrapper.userCancelPrivateTraining, Wrapper.userCancelPublicClass, Wrapper.userReschedulePrivateClass, Wrapper.userManagePayment]
f2 = [Wrapper.trainerSetAvailability, Wrapper.trainerViewUserInformation]
f3 = [Wrapper.adminCreateClassPublic, Wrapper.adminShowAllPublicClasses, 
        Wrapper.adminCreateRoomBooking, Wrapper.adminUpdateRoomBooking, Wrapper.adminDeleteRoomBooking,
        Wrapper.adminMaintainEquipment, Wrapper.adminUpdateBillings]

#userFunctions[loggedInUser][option]
userFunctions = [f1,f2,f3]


def main():
    print("\n\nWelcome to the RD Fitness Club Management System!")
    signInMenu()
    while True:
      sign_in_option = input("Enter your selection: ")
      print("---------------------------------------------------------")
      if sign_in_option=="1":
        signInUser()
        break
      elif sign_in_option=="2":
        signInTrainer()
        break
      elif sign_in_option == "3":
        signInAdmin()
        break
      elif sign_in_option == "4":
        createNewAccount()
        break
      else:
          print("The input you entered was not valid. Please try again.")
    
    #main loop
    while True:
        # call menu function corresponding to logged in user
        # get the # of options that the user can select from
        num_options = menu[loggedInUser]() 
        option = int(input("Selection: "))
        print("---------------------------------------------------------")
        if option >= 1 and option <= num_options:
          if option == num_options:
            sys.exit("Exiting program")
          userFunctions[loggedInUser][option-1](loggedInUserId) if int(loggedInUser) != 2 else userFunctions[loggedInUser][option-1]()
        else:
            print("Invalid input please try again")

def signInUser():
    global loggedInUser, loggedInUserId
    while True:
        print("Please enter the following information: ")
        email = input(" Email: ")
        password = input(" Password: ")
        u_id = User.signIn(email, password)
        if u_id:
            print("Your sign in was successful!")
            loggedInUser = int(UserType.USER)
            loggedInUserId = u_id
            break
        else:
            print("---------------------------------------------------------")
            print("Your sign in was unsuccessful. You may either: ")
            print(" (1) Try again or\n (2) Create a new account or\n (3) Exit")
            print("---------------------------------------------------------")
            unsuc = input("Enter your selection: ")
            print("---------------------------------------------------------")
            if unsuc =="2":
                createNewAccount()
            elif unsuc == "3":
                sys.exit(0)
            else:
                print("Try signing in again.")

def signInTrainer():
    global loggedInUser, loggedInUserId
    while True:
        print("Please enter the following information: ")
        email = input(" Email: ")
        password = input(" Password: ")
        t_id = Trainer.signIn(email, password)
        if t_id:
            print("Your sign in was successful!")
            loggedInUser = int(UserType.TRAINER)
            loggedInUserId = t_id
            break
        else:
            print("---------------------------------------------------------")
            print("Your sign in was unsuccessful. You may either:")
            print(" (1) Try again or\n (2) Exit")
            print("---------------------------------------------------------")
            unsuc = input("Enter your selection: ")
            print("---------------------------------------------------------")
            if unsuc =="2":
                sys.exit(0)
            else:
                print("Try signing in again.")

def signInAdmin():
    global loggedInUser, loggedInUserId
    while True:
        print("Please enter the following information: ")
        email = input(" Email: ")
        password = input(" Password: ")
        a_id = Admin.signIn(email, password)
        if a_id:
            print("Your sign in was successful!")
            loggedInUser = int(UserType.ADMIN)
            loggedInUserId = a_id
            break
        else:
            print("---------------------------------------------------------")
            print("Your sign in was unsuccessful. You may either:")
            print(" (1) Try again or\n (2) Exit")
            print("---------------------------------------------------------")
            unsuc = input("Enter your selection: ")
            print("---------------------------------------------------------")
            if unsuc =="2":
                sys.exit(0)
            else:
                print("Try signing in again.")


def createNewAccount():
    global loggedInUser, loggedInUserId
    print("Please enter the following information to sign up: ")
    name = input(" Full Name (firstname lastname): ").split(" ")
    email = input(" Email: ")
    password = input(" Password: ")
    weight = int(input(" Current Weight (lbs): "))
    height = int(input(" Current Height (cm): "))
    goal = int(input(" Goal Weight (lbs): "))
    User.registerUser(name[0], name[1], email, password, weight, height, goal)

    print("Your account was created. Here is your information: ")
    print(f"Email: {email}, Password: {password}")
    u_id = User.signIn(email, password)
    loggedInUser = int(UserType.USER)
    loggedInUserId = u_id

main()
