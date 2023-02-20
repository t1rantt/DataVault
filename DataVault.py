import os
import argparse
from cryptography.fernet import Fernet

def generate_key(output_path):

    key = Fernet.generate_key()
    with open(output_path, "wb") as key_file:
        key_file.write(key)

def encrypt_image(file_path, key, output_path):

    with open(file_path, "rb") as input_file:
        input_data = input_file.read()

    f = Fernet(key)
    encrypted_data = f.encrypt(input_data)

    with open(output_path, "wb") as output_file:
        output_file.write(encrypted_data)

def decrypt_image(file_path, key, output_path):

    with open(file_path, "rb") as input_file:
        input_data = input_file.read()

    f = Fernet(key)
    decrypted_data = f.decrypt(input_data)
    with open(output_path, "wb") as output_file:
        output_file.write(decrypted_data)

def main():
    parser = argparse.ArgumentParser(description="Encrypt, decrypt and generate AES keys.")

    subparsers = parser.add_subparsers(dest="command", help="Sub-command help")

    generate_key_parser = subparsers.add_parser("generate-key", help="Generate a new key.")
    generate_key_parser.add_argument("-o", "--output", help="Path to save the key.", required=True)

    encrypt_parser = subparsers.add_parser("encrypt", help="Encrypt a file")
    encrypt_parser.add_argument("-f", "--file", help="Path to the file.", required=True)
    encrypt_parser.add_argument("-k", "--key", help="Path to the key.", required=True)
    encrypt_parser.add_argument("-o", "--output", help="Path to output the encoded file", required=True)

    decrypt_parser = subparsers.add_parser("decrypt", help="Decrypt a file.")
    decrypt_parser.add_argument("-f", "--file", help="Path to the file.", required=True)
    decrypt_parser.add_argument("-k", "--key", help="Path to the key.", required=True)
    decrypt_parser.add_argument("-o", "--output", help="Path to output the decoded file", required=True)

    args = parser.parse_args()

    if args.command == "generate-key":
        generate_key(args.output)
        print(f"[*] Generated key saved here: {args.output}")
    if args.command == "encrypt":
        with open(args.key, "rb") as key_file:
            key = key_file.read()
            encrypt_image(args.file, key, args.output)
            print(f"[*] Encrypted data saved here: {args.output}")
    elif args.command == "decrypt":
        with open(args.key, "rb") as key_file:
            key = key_file.read()
            decrypt_image(args.file, key, args.output)
            print(f"[*] Decrypted data saved here: {args.output}")
    else: parser.print_help()

if __name__ == "__main__":
    main()