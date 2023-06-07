from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.fernet import Fernet

# Load the RSA public key from a PEM-encoded file
with open('[Key_Path]', 'rb') as f:
    pem_public_key = f.read()
    public_key = serialization.load_pem_public_key(pem_public_key)

# Load the RSA private key from a PEM-encoded file
with open('[Key_Path]', 'rb') as f:
    pem_private_key = f.read()
    private_key = serialization.load_pem_private_key(pem_private_key, password=b'test')

# Load the Fernet key from a file
with open('[Key_Path]', 'rb') as f:
    fernet_key = f.read()

encrypted_key = public_key.encrypt(
    fernet_key,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

decrypted_key = private_key.decrypt(
    encrypted_key,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

print(fernet_key)
print(encrypted_key)
print(decrypted_key)
