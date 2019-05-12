import sqlite3
from sqlite3 import Error
import csv
from tkinter import *

def createListBox(fileList):
    master = Tk()

    listbox = Listbox(master)
    listbox.pack()

    #listbox.insert(END, "a list entry")

    for item in fileList:#["one", "two", "three", "four"]:
        listbox.insert(END, item)

    mainloop()

# Apparently this code will work in the project directory to create a database if there isn't already one of the specified name.
def create_connection(db_file):
    err = 1
    """ create a database connection to a SQLite database """
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
        return None
    # finally:
    #     conn.close()

    return conn

def create_schema(conn):

    #Create a Database cursor for using the DB
    curs = conn.cursor()

    #Create a table to hold the image data and metadata
    sql = '''CREATE TABLE IF NOT EXISTS buildings
                (PID INTEGER PRIMARY KEY AUTOINCREMENT,
                BOROUGH VARCHAR(100),
                QC VARCHAR (100),
                BLOCKNUMBER INT,
                LOTNUMBER INT,
                BUILDINGNUMBER VARCHAR (100),
                STREETNAME VARCHAR (100),
                ROLLNUMBER VARCHAR (100),
                COMPLETEADDRESS VARCHAR (100),
                CONDITION VARCHAR (100),
                LOTFRONTAGE FLOAT,
                LOTDEPTH FLOAT,
                YEARBUILT INT,
                DATEBUILT VARCHAR (100),
                FILENAME   VARCHAR (100))'''

    curs.execute(sql)

    # Set up variables for holding the individual record values pulled from the csv's
    # Initialize the variables so we know what data type to give them (e.g. string, integer, floating number)
    # These are our Schema Variables
    borough = ""
    qc = '*'
    blocknumber = 0
    lotnumber = 0
    buildingnumber = ""
    streetname = ""
    rollnumber = ""
    completeaddress = ""
    condition = ""
    lotfrontage = 0.0
    lotdepth = 0.0
    yearbuilt = 0
    datebuilt = ""
    filename = ""

    #Open the CSV with Python's CSV reader library
    with open("metadata.csv", newline='') as metadata:
        reader = csv.reader(metadata)
        #skip the first line (headers).  There might be a more elegant way to do this.
        next(reader)

        #Run through the CSV record and assign values to the correct variables.
        #Note: this could be made more readable by using the CSV's column headers as indices
        for row in reader:
            borough = row[1]
            qc = row[2]
            blocknumber = row[3]
            lotnumber = row[5]
            buildingnumber = row[7]
            streetname = row[9]
            rollnumber = row[11]
            completeaddress = row[13]
            condition = row[14]
            lotfrontage = row[17]
            lotdepth = row[18]
            yearbuilt = row[19]
            datebuilt = row[22]
            filename = row[24]

            #create a record in the database for each row in the CSV
            curs.execute(
                "INSERT INTO buildings (BOROUGH, QC, BLOCKNUMBER, LOTNUMBER, BUILDINGNUMBER, STREETNAME, ROLLNUMBER, COMPLETEADDRESS, CONDITION, LOTFRONTAGE, LOTDEPTH, YEARBUILT, DATEBUILT, FILENAME) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", \
                (
                borough, qc, blocknumber, lotnumber, buildingnumber, streetname, rollnumber, completeaddress, condition,
                lotfrontage, lotdepth, yearbuilt, datebuilt, filename))

            #Don't forget we have to commit any changes we make to records.
            conn.commit()

    #Don't forget to close the DB connection before we leave
    conn.close()
    return 0

if __name__ == '__main__':
    conn = create_connection("taxphotos.db")
    fileList = ['one', 'two', 'three', 'four']
    createListBox(fileList)
    #if conn:
    #    create_schema(conn)


# from {input selection} open
#
# filename = "nynyma_rec0040_1_00993_0001"
#
# open("./Images/" + filename + ".jpg")