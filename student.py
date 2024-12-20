import sqlite3
import config
import random
from tabulate import tabulate

class Students:
    # Add a connection to the database to the object
    def __init__(self, database):
        self.database = database
        self.cursor = database.cursor()

    # Generate a registration ID for a student (it's just a random alphanumeric string)
    def generateRegID(self):
        id = ""
        prefix = config.SCHOOLNAME[0:3].upper() # Use the first 3 letters of the name of the school as part of the registration ID
        id += prefix
        for i in range(9):
            id += str(random.randint(0, 9))
        return id

    def newStudent(self):
        from project import requestUserInput, checkEmail
        # Input fields to type in student details
        try:
            # Query to insert the new student details into the "students" database table.
            newStudentQuery = "INSERT INTO students (studentRegId, studentName, studentAddress, studentEmail, studentPhone) VALUES (?, ?, ?, ?, ?)"
            searchStudentByNameQuery = "SELECT * FROM students WHERE studentName = ?" # Search for a student with the specified name
            searchStudentByEmailQuery = "SELECT * FROM students WHERE studentEmail = ?" # Search for a student with the specified email address

            print("---------------------------------------------------------")
            print("Add a new student")
            print("If you want to go back to the menu, click 'CTRL' + 'C'")
            print("---------------------------------------------------------")
            while True:
                name = requestUserInput("Student's name: ", 1)
                if len(self.cursor.execute(searchStudentByNameQuery, [name]).fetchall()) == 0: # Check if the name is currently stored in the database
                    break
                else:
                    print("That student name already exists. Please select a different name")

            address = requestUserInput("Student's home address: ", 1)

            while True:
                email = requestUserInput("Student's email address: ", 1)
                if len(self.cursor.execute(searchStudentByEmailQuery, [email]).fetchall()) == 0: # Check if the email address is currently stored in the database
                    emailCheck = checkEmail(email)
                    if emailCheck:
                        break
                    else:
                        print("Please enter a valid email address. Format: johndoe@example.com.")
                else:
                    print("That student email already exists. Please select a different email address.")

            phone = requestUserInput("Student's phone number: ", 1)
            registrationID = self.generateRegID()

            # Check if the user has entered a valid email address
            emailCheck = checkEmail(email)

            # Insert the new student details
            self.cursor.execute(newStudentQuery, [registrationID, name, address, email, phone])
            self.database.commit() # Save the changes made in the database

            print(f"Student \"{name}\" has been added to the database successfully.")
        except KeyboardInterrupt:
            print("Exiting to the menu...")


    def updateStudentDetails(self, currentDetails):
        from project import requestUserInput, checkEmail
        # Dictionary to store the newly entered details as well as prompt messages and SQL queries to use with the database
        detailsConfig = {
            "name": {
                "promptMessage": "New name: ",
                "updateQuery": "UPDATE students SET studentName = ? WHERE id = ?",
                "updateSuccessMessage": "Name updated successfully",
                "new": None
            },
            "address": {
                "promptMessage": "New address: ",
                "updateQuery": "UPDATE students SET studentAddress = ? WHERE id = ?",
                "updateSuccessMessage": "Address updated successfully",
                "new": None
            },
            "email": {
                "promptMessage": "New email address: ",
                "updateQuery": "UPDATE students SET studentEmail = ? WHERE id = ?",
                "updateSuccessMessage": "Email address updated successfully",
                "new": None
            },
            "phone": {
                "promptMessage": "New phone number: ",
                "updateQuery": "UPDATE students SET studentPhone = ? WHERE id = ?",
                "updateSuccessMessage": "Phone number updated successfully",
                "new": None
            }
        }
        while True:
            try:
                print("----------------------------------------------")
                detailsChoice = requestUserInput("Which detail do you want to modify?\n'name'\n'address'\n'email'\n'phone'\nIf you want to save changes and exit, type 'save'.\nIf you want to exit without saving changes, click 'CTRL' + 'C'\nCommand: ", 1)

                if detailsChoice.lower() in detailsConfig:
                    newDetailInput = requestUserInput(detailsConfig[detailsChoice.lower()]["promptMessage"], 1) # Prompt user to enter the new details
                    if detailsChoice.lower() == "email": # Check if the email address entered is in a correct format
                        if not checkEmail(newDetailInput):
                            print("Invalid email address entered. Please try again.")
                    detailsConfig[detailsChoice.lower()]["new"] = newDetailInput

                elif detailsChoice.lower() == "save":
                    # Insert the new details into this array
                    newDetails = [i[1]["new"] for i in list(detailsConfig.items())]

                    updateQueries = [i[1]["updateQuery"] for i in list(detailsConfig.items())]
                    successMessages = [i[1]["updateSuccessMessage"] for i in list(detailsConfig.items())]

                    # Check if there are any values in the array aside from "None"
                    # This will check whether there are changes made with any of the details
                    if any(newDetails):
                        for i in range(len(newDetails)):
                            # Ignore if one of the values in the "newDetails" array is "None"
                            # This will prevent "None" values in the array from being written to the database
                            if not newDetails[i]:
                                continue
                            else:
                                # Run the queries stored in "updateQueries" to write the new details to the current student in the database
                                if self.cursor.execute(updateQueries[i], [newDetails[i], currentDetails[0][0]]):
                                    print(successMessages[i])

                        self.database.commit()
                        break
                    else:
                        print("You haven't made any changes. Please do so before proceeding.")

                else:
                    print("Invalid input. Please try again.")

            except ValueError:
                return None
            except KeyboardInterrupt:
                print("Exiting to the menu...")


    def deleteStudentDetails(self, details):
        from project import requestUserInput
        while True:
            print("---------------------------------------------------------")
            # Prompt user for confirmation to delete student details
            deleteConfirm = requestUserInput(f"Are you sure you want to delete {details[0][2]}'s details? (type 'Y' for yes, 'N' for no)", 1)
            if deleteConfirm.lower() == "y":
                deleteQuery = "DELETE FROM students WHERE id = ?"

                # Run the query deleting student details
                if self.cursor.execute(deleteQuery, [details[0][0]]):
                    print(f"Details of '{details[0][2]}' have been deleted successfully")
                    break
            elif deleteConfirm.lower() == "n":
                break
            else:
                print("Invalid input. Please try again.")


    def getStudent(self):
        from project import requestUserInput
        while True:
            try:
                print("---------------------------------------------------------")
                print("Get student details")
                print("If you want to go back to the menu, click 'CTRL' + 'C'")
                print("---------------------------------------------------------")

                name = requestUserInput("Enter a student's registration ID: ", 1) # Prompt user to type in a student's name
                searchStudentQuery = "SELECT * FROM students WHERE studentRegId = ?"
                if len(self.cursor.execute(searchStudentQuery, [name]).fetchall()) != 0: # Check if the result of the query returned any rows
                    details = self.cursor.execute(searchStudentQuery, [name]).fetchall()
                    print("----------------------------------------------")
                    print("Here are the details of the student: ")
                    print("----------------------------------------------")
                    # Print out the student details fetched from the database
                    for i in range(len(details)):
                        print(f"Name: {details[i][2]}")
                        print(f"Address: {details[i][3]}")
                        print(f"Email address: {details[i][4]}")
                        print(f"Phone number: {details[i][5]}")
                    print("----------------------------------------------")
                    # Prompt the user to either edit or delete user details
                    detailsCommand = requestUserInput("What do you want to do with these details?\n'edit' - Edit the existing details\n'delete' - Remove it from the system permanently\n'exit' - Go back to the main menu\nCommand: ", 1)
                    match detailsCommand.lower():
                        case "edit":
                            self.updateStudentDetails(details)
                            break
                        case "delete":
                            self.deleteStudentDetails(details)
                            break
                        case "exit":
                            break
                        case _:
                            continue
                else:
                    print("That student does not exist in the database. Please try another.")
            except KeyboardInterrupt:
                print("Exiting to the menu...")
                break


    def getAllStudents(self):
        # Store the table headers to name each column
        tableHeaders = ["Registration ID", "Name", "Address", "Email address", "Phone"]

        allStudentsQuery = "SELECT * FROM students"

        # Get all the student details and store it in an array
        allDetails = self.cursor.execute(allStudentsQuery).fetchall()

        # Convert the array "allDetails" into a table format and add the respective headers
        if len(allDetails) != 0:
            print(tabulate(allDetails, tableHeaders, tablefmt="grid"))
        else:
            print("There are currently no students in the database. You can add one by typing 'addstudent' in the main menu.")

        input("Press 'Enter' to exit...")