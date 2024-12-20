'''
Command-line based student management system

Created by: mantot123
Course: CS50P - Introduction to Programming in Python
'''

import sqlite3
import config
import re
import student
import grade

# Save the current connection to the database
sqlDb = sqlite3.connect("studentmanagerdb.sqlite3")

# Add a cursor to be able to run queries on the database
sqlCursor = sqlDb.cursor()

# Prompt the user for input. Parameters:
# "message" - Message to be printed out to ask the user for input
# "type" - Determines the type of data to be entered (1 for text, 2 for a either an integer or a decimal number)
def requestUserInput(message, type):
    if type == 1: # Request user to enter a string (text)
        while True:
            text = input(message)
            if text != "":
                return text
            else:
                print("This field cannot be left empty. Please enter something.")
    elif type == 2: # Request user to enter a number
        while True:
            try:
                number = float(input(message))
                return number
            except ValueError:
                print("Please enter a valid number.")


def checkEmail(email):
    # Check if the email address is entered in a correct format. Example: johndoe@example.com
    # "r" needs to be placed before the regex string so that the interpreter treats characters like '\n' as just normal text with no special functionality
    emailPattern = r"^[a-zA-Z0-9]+[^@]+@[a-zA-Z0-9]+[^@]+\.[a-zA-Z0-9]+[^@]+$"
    if re.search(emailPattern, email):
        return True


def promptExit():
    while True:
        exitConfirm = requestUserInput("Are you sure you want to exit? (Y for yes, N for no)\n", 1)
        if exitConfirm.lower() == "y":
            exit()
        elif exitConfirm.lower() == "n":
            break
        else:
            print("Invalid input.")


def main():
    if (config.SCHOOLNAME == "") or (not config.SCHOOLNAME):
        print("Error: You haven't set a name for your school yet!")
        print("To set one, go to 'config.py' and change the 'SCHOOlNAME' variable with the name of your school.")
        print("Make sure that the name of your school is surrounded with quotation marks!")
        exit(1)
    else:
        while True:
            try:
                studentManager = student.Students(sqlDb)
                gradeManager = grade.Grades(sqlDb)
                print("---------------------------------------------------------")
                command = input("Welcome to Studz, a Student Management System.\nWhat do you want to do?\n'addstudent' - Add a new student\n'getstudent' - Get the details of an existing student\n'allstudents' - View details of all students\n'addgrade' - Add a grade\n'getgrades' - Get the grades of a student\n'exit' or clicking 'CTRL + C' - Exit the program\nCommand: ")
                match command.lower():
                    case "addstudent":
                        studentManager.newStudent()
                    case "getstudent":
                        studentManager.getStudent()
                    case "allstudents":
                        print("Here are the details of all of the students: ")
                        studentManager.getAllStudents()
                    case "getgrades":
                        gradeManager.getStudentGrades()
                    case "addgrade":
                        gradeManager.addGrade()
                    case "exit":
                        promptExit()
                    case _: # Execute this whenever the user enters something else (an invalid command)
                        print("Invalid command. Please try again.")
            except EOFError:
                promptExit()
            except KeyboardInterrupt:
                promptExit()


if __name__ == "__main__":
    main()

