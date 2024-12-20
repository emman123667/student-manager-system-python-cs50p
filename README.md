# CS50 Final Project
## Project: Student management system

Created by: Emman Ruiz Medina

Video demo: https://www.youtube.com/watch?v=Y1_kBmj0SAE

Hello, world! In this final project, I have created a student management system used for managing student details and grades for different subjects.

Requirements:
*  Python 3.10
*  "sqlite3" - For the database
*  "random" - For generating random alphanumeric strings. Used in generating new registration IDs
*  "re" - To use regular expressions to validate email addresses
*  "tabulate" - Get student details and grades and display them in a readable format

## Database schema

Students:
```
CREATE TABLE students (
    id INTEGER,
    studentRegId TEXT,
    studentName TEXT,
    studentAddress TEXT,
    studentEmail TEXT,
    studentPhone TEXT,
    PRIMARY KEY(id)
);
```

Grades:
```
CREATE TABLE grades(
    id INTEGER,
    grade TEXT,
    marksGained INTEGER,
    maxMarks INTEGER,
    classSubject TEXT,
    studentId INTEGER, -- Foreign key. This will reference an existing student in the "students" database table by their primary key
    PRIMARY KEY(id)
);
```

## config.py

This is the configuration file that is imported in the main program (project.py). Inside the file, there is a variable called "SCHOOLNAME". This will store the name of the school that can be used to generate registration IDs for new students.

How to change:<br>
``SCHOOLNAME = "<school name>"``<br>
``SCHOOLNAME = "Harvard University"``

Remember to always surround the name of your school with quotation marks ("")!

There is also another variable called "GRADES". This stores the percentages needed to get to achieve a certain grade. The variable will look like this in the file by default. The actual grade is stored on the left column where you can see the grades "A", "B", "C" etc., while the percentage needed to get them is stored on the right column:
```
GRADES = {
    "A": 0.90,
    "B": 0.70,
    "C": 0.60,
    "D": 0.50,
    "E": 0.30,
    "F": 0.10,
}
```

## student.py

This is used to handle student details and store them in the database. It has several methods to handle adding, retrieving, ediing and deleting student details from the database.

## grade.py

This is used to handle student grades. It has methods to handle adding and retrieving student grades from the database.

## project.py

This is the main file and it contains the entire functionality and interface of the program. It consists of several methods to handle user input, and it imports the rest of the files within the project directory to put everything together



### How to use this program

![screenshot of commands that can be used in the program](screenshot1.PNG)

This is the main menu, which is the first page you will see as you open the program. This will display the list of commands that you can use to interact with the program. Below the list, there's an input field where you can type a command. Here's how each of the commands work:

* **addstudent** - This will take you to a page where you can add a new student to the database. This will require you to set a name, home address, email address and a phone number. The system will check if the email address is entered in a correct format (example: johndoe@example.com). From there, both the student name and email address will be checked if they're currently stored in the database. If so, it will display an error requesting you to enter a different name and email address. If not, the system will automatically generate a new registration ID and store all of the new details including the ID in the database

* **getstudent** - This will take you to a page where you can enter a student's registration ID to get all of their details. If the registration ID entered exists in the database, the system will display all of the details and it will give you 3 options: "edit", "delete" or "exit"
  * **edit** - This will open a page where you can choose which one of the student details to edit. You can choose to modify either the student's name, home address, email address or phone number. When you're done, you can then choose to save changes and exit or exit without saving them.
  * **delete** - This will display a confirmation message asking you whether you want to delete all of the details associated with the student from the database
  * **exit** - Exit to the main menu
* **allstudents** - This will display all of the student's details in the form of a table
* **addgrade** - Add a grade. This will prompt users to type a grade, number of marks received in a test, the maximum number of marks, the subject, as well as the student registration ID to add this grade to.
* **getgrades** - Prompt the user for a student's registration ID and display all of the student's grades in a table format


## Keyboard shortcuts available

* "CTRL" + "D" - Exit the program/Exit to the main menu

## Additional features that can be added
Here are some of the features that can be added to the student management system to improve it further:
* **Graphical User Interface (GUI)** - Instead of having the program run on the terminal, we can use libraries like Tkinter or PyQt to make the program easy to use and interact with
* **Web technologies** - The program can also be run as a website using web frameworks like Flask and languages like HTML, CSS and JavaScript. Also great for building a GUI
* **Classes** - Users can create classes where students can be added and grouped. To add on to this further, users can also assign grades to students for each class they take
* **Progress system** - Progress of students for each week, term or semester can be saved and then displayed in the form of a graph so they can be viewed. Best added with a GUI.
* **More advanced grading system** - The program can be configured so that grades are automatically given based on percentage of marks received. (THIS IS ADDED IN THIS NEW VERSION)


## Acknowledgements

I would like to thank David J. Malan and the whole team for letting me be part of this CS50 Python course and offering me to create this final project. It allowed me to expand my programming and problem solving skills further while also motivating me to keep my passion for programming alive.
