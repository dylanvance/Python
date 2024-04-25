"""
Lab 4
Dylan Vance
"""
import tkinter as tk
from tkinter import Tk
from tkinter import messagebox
import sqlite3 as sql


# Student Database Class
# Creates Student table. Supports insert, update, select *
class StudentDatabase:
    def __init__(self):
        self.connection = sql.connect("dbGUI.db")
        self.cursor = self.connection.cursor()

    def createTable(self):
        # STD_ID (INTEGER), STD_NAME (TEXT), STD_EMAIL (TEXT), STD_GPA (REAL).
        student_table = """CREATE TABLE STUDENTS(
        STD_ID INTEGER NOT NULL,
        STD_NAME TEXT NOT NULL,
        STD_EMAIL TEXT NOT NULL,
        STD_GPA REAL NOT NULL,
        PRIMARY KEY (STD_ID)
        );"""

        try:
            self.cursor.execute(student_table)
        except sql.OperationalError:
            pass

    def insertRecord(self, Id, Name, Email, Gpa):
        try:
            self.cursor.execute("INSERT INTO STUDENTS (STD_ID, STD_NAME, STD_EMAIL, STD_GPA) VALUES (?, ?, ?, ?)", (Id, Name, Email, Gpa))
            self.connection.commit()
            return True
        except sql.OperationalError:
            return False

    def updateRecord(self, Id, Name, Email, Gpa):
        try:
            self.cursor.execute("UPDATE STUDENTS SET STD_NAME = ?, STD_EMAIL = ?, STD_GPA = ? WHERE STD_ID = ?", (Name, Email, Gpa, Id))
            self.connection.commit()
            return True
        except sql.OperationalError:
            return False

    def dataRecord(self):
        self.cursor.execute("SELECT * FROM STUDENTS")
        return self.cursor.fetchall()

    def closeConnection(self):
        self.connection.close()


# Creates all widgets and popup windows
# Calls the database functions in StudentDatabase class
class StudentData(Tk):
    def __init__(self):
        super().__init__()
        self.Id = tk.IntVar(self)
        self.Name = tk.StringVar(self)
        self.Email = tk.StringVar(self)
        self.Gpa = tk.DoubleVar(self)
        self.Db = StudentDatabase()
        self.geometry("500x500")
        self.title("Student Management System")

    def createStudentTable(self):
        self.Db.createTable()

    def createLabel(self, rowNum, colNum, labelText):
        label = tk.Label(self, text=labelText)
        label.grid(row=rowNum, column=colNum, padx=5, pady=5)

    def createEntry(self, rowNum, colNum, fieldName):
        if fieldName == 'Id':
            textVariable = self.Id
        elif fieldName == 'Name':
            textVariable = self.Name
        elif fieldName == 'Email':
            textVariable = self.Email
        elif fieldName == 'Gpa':
            textVariable = self.Gpa
        else:
            textVariable = None
        entry = tk.Entry(self, textvariable=textVariable)
        entry.grid(row=rowNum, column=colNum, padx=5, pady=5)

    def createTextArea(self, rowNum, colNum, text):
        text_area = tk.Text(self, height=25, width=50)
        text_area.grid(row=rowNum, column=colNum, padx=5, pady=5)
        for line in text:
            text_area.insert(tk.END, line)
            text_area.insert(tk.END, "\n")

    def createButton(self, rowNum, colNum, title, function):
        if function == 'addStudent':
            button = tk.Button(self, text=title, command=self.addStudent)
            button.grid(row=rowNum, column=colNum, padx=5, pady=5)
        elif function == 'updateStudent':
            button = tk.Button(self, text=title, command=self.updateStudent)
            button.grid(row=rowNum, column=colNum, padx=5, pady=5)
        elif function == 'displayStudent':
            button = tk.Button(self, text=title, command=self.displayStudent)
            button.grid(row=rowNum, column=colNum, padx=5, pady=5)
        else:
            print("Pass a proper function. Button not created")

    def addStudent(self):
        add_window = StudentData()
        add_window.createLabel(0, 0, "Add Student")
        add_window.createLabel(1, 0, "Student ID: ")
        add_window.createEntry(1, 1, "Id")
        add_window.createLabel(2, 0, "Student Name: ")
        add_window.createEntry(2, 1, "Name")
        add_window.createLabel(3, 0, "Student Email: ")
        add_window.createEntry(3, 1, "Email")
        add_window.createLabel(4, 0, "Student GPA")
        add_window.createEntry(4, 1, "Gpa")
        add_button = tk.Button(add_window, text="Add", command=add_window.insertRecord)
        add_button.grid(row=5, column=1, padx=5, pady=5)

    def insertRecord(self):
        self.destroy()
        self.Db.insertRecord(self.Id.get(), self.Name.get(), self.Email.get(), self.Gpa.get())

    def updateStudent(self):
        update_window = StudentData()
        update_window.createLabel(0, 0, "Update Student")
        update_window.createLabel(1, 0, "Student ID: ")
        update_window.createEntry(1, 1, "Id")
        update_window.createLabel(2, 0, "Student Name: ")
        update_window.createEntry(2, 1, "Name")
        update_window.createLabel(3, 0, "Student Email: ")
        update_window.createEntry(3, 1, "Email")
        update_window.createLabel(4, 0, "Student GPA")
        update_window.createEntry(4, 1, "Gpa")
        update_button = tk.Button(update_window, text="Update", command=update_window.updateRecord)
        update_button.grid(row=5, column=1, padx=5, pady=5)

    def updateRecord(self):
        self.destroy()
        self.Db.updateRecord(self.Id.get(), self.Name.get(), self.Email.get(), self.Gpa.get())

    def displayStudent(self):
        display_window = StudentData()
        display_window.createLabel(0, 0, "Student Records")
        text = self.Db.dataRecord()
        display_window.createTextArea(1, 0, text)


# Main function
# Creates the main window
if __name__ == '__main__':
    data = StudentData()
    data.createStudentTable()
    data.createLabel(0, 0, "Student Management System")
    data.createButton(1, 0, "Add Student", "addStudent")
    data.createButton(2, 0, "Update Student", "updateStudent")
    data.createButton(3, 0, "Display Student", "displayStudent")
    data.mainloop()
