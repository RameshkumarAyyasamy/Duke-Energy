Install the required packages:
Python 3.9.6
pip3
imagehash
Pillow
requests==2.32.3


DB:
sqlite3

To Run:
Execute the code with the command "python main.py". 
The camera will be turned on; press "S" on your keyboard to capture the image. It will be stored in JSON. 
The JSON data will be compared with the database data and will indicate any duplicates or threats. Duplicates will not be stored in the database.