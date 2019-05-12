
# provides disk-based database, doesn’t require a server process, allows accessing the database using SQL query language
import sqlite3

# NOTE: requires Pillow library (should be in Anaconda) https://pillow.readthedocs.io/en/stable/installation.html
from PIL import Image

# function that tailors down image filename to the respective folder id
def getFoldername( filename ):
	filenameSegments = filename.split("_")
	foldername = filenameSegments[3].replace("00", "")
	return foldername

# connect to the database (include path if db is in different directory)
conn = sqlite3.connect('pythonsqlite.db')

# create a cursor object
cur = conn.cursor()

# ask the user for an address like e.g. 561-565 7 Avenue
completeaddress = input("Please enter an exact street address (e.g. 561-565 7 Avenue): ")
#completeaddress = '561-565 7 Avenue'

# search the address field for the image file name
t = (completeaddress,)
cur.execute("SELECT FILENAME FROM buildings WHERE COMPLETEADDRESS =?", t )

# return an image from the database that contains the street address
filenames = cur.fetchall()


for filename in filenames:
	# get folder name through tailoring the filename on first position of tuples
	foldername = getFoldername(filename[0])

	# build relative path to the image file
	relativeDir = "Images" + "\\"  + filename[0] + ".jpg"

	# load the image   
	image = Image.open(relativeDir)

	# show image file
	image.show()

	# close loaded image file
	image.close()

# close connection to db
conn.close()