import sqlite3
from tabulate import tabulate
import config

class Grades:
    # Add a connection to the database to the object
    def __init__(self, database):
        self.database = database
        self.cursor = database.cursor()
    
    def addGrade(self):
        from project import requestUserInput
        try:
            print("---------------------------------------------------------")
            print("Add a grade to a student")
            print("If you want to go back to the menu, click 'CTRL' + 'C'")
            print("---------------------------------------------------------")
            
            # Check if the grades are set in the "config.py" file
            gradesConfigured = config.GRADES != None or config.GRADES != {}

            # If the grades are not configured, prompt the user to enter a grade manually
            if not gradesConfigured:
                grade = requestUserInput("Enter the grade received: ", 1)

            while True:
                # Prompt the user to enter the number of marks received
                marks = requestUserInput("Enter the number of marks received: ", 2)
                maxMarks = requestUserInput("Maximum number of marks possible: ", 2)

                # Check if the number of marks received is less than the maximum number of marks possible
                if marks > maxMarks:
                    print("Error: Number of marks received have to be smaller than or the same as the maximum marks.")
                    continue
                
                if gradesConfigured:
                    marksRatio = marks / maxMarks
                    for currentGrade, percentage in list(config.GRADES.items()):
                        # If the percentage in the config file currently being checked meets the percentage of marks entered by the user, assign the user the current grade
                        if percentage <= marksRatio:
                            grade = currentGrade
                            break
                        else: # If percentage entered by the user meets none of the percentages in the config file, assign the user the grade with the lowest percentage
                            grade = list(config.GRADES.items())[-1]
                    
                break
                

            subject = requestUserInput("Enter the subject: ", 1)

            while True:
                student = requestUserInput("Student Registration ID to add this grade to: ", 1)
                searchStudentIDQuery = "SELECT id FROM students WHERE studentRegId = ?"
                # Check if the student exists in the database before adding the grade
                if len(self.cursor.execute(searchStudentIDQuery, [student.strip()]).fetchall()) != 0:
                    studentDbId = self.cursor.execute(searchStudentIDQuery, [student.strip()]).fetchall()[0][0]
                    break
                else:
                    print("That student is not found in the database. Please try another ID.")

            # Insert the new grade into the the database
            addGradeQuery = "INSERT INTO grades (grade, marksGained, maxMarks, classSubject, studentId) VALUES (?, ?, ?, ?, ?)"
            self.cursor.execute(addGradeQuery, [grade, marks, maxMarks, subject, studentDbId])

            print("This grade is successfully added to this student's record")
            self.database.commit()

        except KeyboardInterrupt:
            print("Exiting to the menu...")


    def getStudentGrades(self):
        from project import requestUserInput
        try:
            while True:
                print("---------------------------------------------------------")
                print("Get student grades")
                print("If you want to go back to the menu, click 'CTRL' + 'C'")
                print("---------------------------------------------------------")
                student = requestUserInput("Enter a student's registration ID: ", 1)

                # Make all the letters in the registration ID uppercase so it's case-insensitive
                student = student.upper()

                # Search for a student's name and primary key with the specified registration ID
                searchStudentIDQuery = "SELECT id, studentName FROM students WHERE studentRegId = ?"

                # Get all of the grades and marks of the student
                gradesQuery = "SELECT grade, marksGained, maxMarks, classSubject FROM grades WHERE studentId = ?"

                # Run the search student query to check if the student exists in the database first before displaying all of the grades
                runSearchStudent = self.cursor.execute(searchStudentIDQuery, [student]).fetchall()
                if len(runSearchStudent) != 0:
                    gradesTableHeaders = ["Grade", "Marks", "Max. marks", "Subject"]
                    studentDbId = runSearchStudent[0][0]
                    studentDbName = runSearchStudent[0][1]
                    fullGrades = self.cursor.execute(gradesQuery, [studentDbId]).fetchall()
                    if len(fullGrades) != 0:
                        print(f"Here are {studentDbName}'s grades:")
                        print(tabulate(fullGrades, headers=gradesTableHeaders, tablefmt="grid")) # Display all the student's grades in a table format
                    else:
                        print("There are currently no grades for this student. You can add one by typing 'addgrade' in the main menu.")
                    input("Press 'Enter' to exit...")
                    break
                else:
                    print("That student is not found in the database. Please try another ID.")

        except KeyboardInterrupt:
            print("Exiting to the menu...")