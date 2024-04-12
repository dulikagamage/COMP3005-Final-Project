# COMP3005 Final Project
## Authors:   
 Dulika Gamage - 101263208  
 Ray Fan       - 101260632  
## Program Description:   
This program replicates a Fitness club with Members, Trainers, and Administrative Staff.     
## ⚙️ Create the Database:  
Ensure PostgreSQL is running on your localhost.    
In pgAdmin4, create a database called "Final"   
In the provided db_conn.py file, change the username and password to your corresponding username and password on pgAdmin4.  
Here is what the line should look like, where 'username' and 'password' would be your username and password  

      db = Database('localhost', 'Final', 'username', 'password', 5432)

⚠️ Ensure these values are correct as they are loaded into the rest of the application and necessary for it to run correctly.  

Once that is done use the DDL.sql and DML.sql (located in SQL folder) to run queries in pgAdmin4 to set up the database.  

## ▶️ Compiling and Running the Program:
Verify that you have Python by running the following command in your terminal:
  
      python --version
  Also, install the following if you do not have it already. In your terminal enter:
  
      pip3 install psycopg2  
Navigate to the directory where this project is stored.  
In your command line or terminal enter the following:  

      python main.py  
Once the program is running you may follow the video demonstration for further instruction.  

## Video Demonstration:
  https://youtu.be/rGnQ8RC1tVw
