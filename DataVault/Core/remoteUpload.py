import os
import argparse
from cryptography.fernet import Fernet
import mysql.connector


config = {
    'user': '[username]',
    'password': '[password]',
    'host': '[HOST IP]',
    'port': '[SQL PORT]',
    'database': '[DB NAME]'
}

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", required=True, help="MySQL username")
parser.add_argument("-p", "--password", required=True, help="MySQL password")
parser.add_argument("-c", "--column", required=True, choices=["user_id", "first_name", "middle_name", "last_name", "email", "address", "dni", "driver_license", "weapon_license", "banking_data", "medical_data", "phone_number", "ip_address", "date_of_birth", "race", "gender", "cookies"], help="column name to insert data into")
parser.add_argument("-i", "--input-file", required=True, help="path to input file")
parser.add_argument("-k", "--input-key", required=True, help="key to extract data from input file")
args = parser.parse_args()

cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()

query = ("SELECT id FROM login WHERE username = %s AND password = %s")
values = (args.username, args.password)
cursor.execute(query, values)
user_id = cursor.fetchone()
if user_id:
	id = user_id[0]
else:
	print("Wrong credentials")

with open(args.input_file, 'rb') as f:
    data = f.read()


with open(args.input_key, 'rb') as f:
    key = f.read()

f = Fernet(key)

encrypted_data = f.encrypt(data)
encrypted_data = encrypted_data.decode('utf-8')

# insert the input data into the specified column for the user ID
query = "UPDATE user_data SET {} = %s WHERE id = %s".format(args.column)
cursor.execute(query, (encrypted_data, id))

# commit the changes and close the database connection
cnx.commit()
cursor.close()
cnx.close()


