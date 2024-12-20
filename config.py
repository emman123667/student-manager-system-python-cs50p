# Configuration settings for the program

# Name of the school. This will be used in generating registration IDs for new students
SCHOOLNAME = "Harvard University"


'''
Grade boundary system. This will allow the program to automatically assign grades based on percentage of marks that the students got

You can change the minimum percentage of marks by changing the decimal number on the right
Example: If you want to change the percentage to get a grade A at 90% or above, change:
"A": 1.00 
to:
"A": 0.90

You can also change the grade letter by changing the text/letter wrapped in quotation marks on the left to any other text/letter that you want
Example: If you want to change the grade letter to "B" from "A", simply change:
"A": 0.90
to:
"B": 0.90

If you don't want to use the grade boundary system and instead set grades manually yourself, simply set the GRADES variable to "None" or "{}"
Example:
GRADE = {}
GRADE = None
'''
GRADES = {
    "A": 0.90,
    "B": 0.70,
    "C": 0.60,
    "D": 0.50,
    "E": 0.30,
    "F": 0.10,
}