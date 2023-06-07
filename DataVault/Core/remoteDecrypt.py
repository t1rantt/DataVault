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
parser.add_argument("-o", "--output-file", required=True, help="path to input file")
parser.add_argument("-k", "--key", required=True, help="key to extract data")
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

query = f"SELECT {args.column} FROM user_data WHERE id = %s"
values = (id,)
cursor.execute(query, values)
data = cursor.fetchone()[0]

if data is None:
	print("NULL")
	exit()
else:
	
    	f = Fernet(args.key.encode('utf-8'))
    	decrypted_data = f.decrypt(data.encode('utf-8'))
    	with open(args.output_file, "wb") as output_file:
        	output_file.write(decrypted_data)
        	
print("[*] File generated")



cnx.commit()
cursor.close()
cnx.close()
exit()

