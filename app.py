import sqlite3
from sqlite3 import Error
import csv
from tkinter import *
#import showcase
from PIL import Image

def createListBox(addressList, conn):
    master = Tk()
    master.title("Select an address from the following list")
    curs = conn.cursor()

    def showPicture():
        value = str((listbox.get(ACTIVE)))

        curs.execute("SELECT FILENAME FROM buildings WHERE COMPLETEADDRESS=?", (value,))
        filenames = curs.fetchall()

        # build relative path to the image file
        relativeDir = "Images" + "\\" + filenames[0][0] + ".jpg"
        # load the image
        image = Image.open(relativeDir)
        # show image file
        image.show()

    # set up the window parameters
    sizex = 600
    sizey = 400
    posx = 40
    posy = 20
    master.wm_geometry("%dx%d+%d+%d" % (sizex, sizey, posx, posy))
    lbl = Label(master,text = "Select an address to view")

    # add a listbox inside the window
    listbox = Listbox(master, width=60,height=10)

    # populate the listbox with all the addresses that we passed into the function
    for item in addressList:#["one", "two", "three", "four"]:
        listbox.insert(END, item)
    listbox.pack()
    lbl.pack()

    # add a button that calls our callback function showPicture which is defined above
    btn = Button(master, text="View", command=showPicture)
    btn.pack()

    # calling mainloop() makes sure our window stays up until we close it
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

    #Don't forget to close the DB connection before we leave -- if no other functions are called in "main"
    conn.close()
    return 0

def getAddresses(conn):
    # create a cursor object
    cur = conn.cursor()

    # run a query to get all the records in the buildings table
    cur.execute("SELECT * FROM buildings")

    # declare variable to hold the addresses
    addresses = []

    # create a data object to store all query results
    data = cur.fetchall()

    # populate the address list by reading in the COMPLETE ADDRESS field
    for addy in data:
        addresses.append(addy[8])

    return addresses


if __name__ == '__main__':
    conn = create_connection("taxphotos.db")

    # uncomment these lines to rebuild the database.
#    if conn:
#        create_schema(conn)

    # the first line populates a list with all of the complete addresses from the db
    # the second line runs the GUI
    # these could be condensed to "createListBox(getAddresses(conn), conn)"
    addressList = getAddresses(conn)
    createListBox(addressList, conn)

    # always ensure that the connection to the db gets closed.
    conn.close()