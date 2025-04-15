from cryptography.fernet import Fernet
import json
import time
import os

key_file = "C:\\Users\\ktmcw\\Desktop\\key.key"
path = "C:\\Users\\ktmcw\\Desktop\\json_token.json"

def save_key(key, key_file_path):

    try:
        with open(key_file_path, "wb") as file:
            file.write(key)
        print("key saved")
    except Exception as e:
        print("failed to save key")

def get_key(key_path):
    try:
        if os.path.exists(key_path):  # check if the file exists
            with open(key_path, "rb") as file:
                key = file.read()
                print("key loaded")
                return key
        else:
            # if it doesnt make a new one
            print("generating new key")
            key = Fernet.generate_key()
            save_key(key, key_path)
            return key

    except Exception as e:
        print("failed to retrieve key: {e}")
        return None

def check_token_expired(expiry_time) -> bool:
    # check if its expired
    return time.time() > expiry_time

def save_token_to_file(token, filename, key_path):
    key = get_key(key_path)

    if key:
        fernet_thing = Fernet(key) # create a fernet object for encryption/decryption
        data = json.dumps(token).encode()
        enc = fernet_thing.encrypt(data)

        with open(filename, "wb") as file:
            file.write(enc)
        print("encrypted token saved to file")

    else:
        print("no valid key found")

def load_token_from_file(filename, key_path):
    try:
        key = get_key(key_path)

        if key: #make sure the key is valid
            fernet_thing = Fernet(key)

            with open(filename, "rb") as file:
                data_enc = file.read()
                data = fernet_thing.decrypt(data_enc)
                data = json.loads(data.decode())  # convert decrypted to json
                print(f"token loaded and decrypted from {filename}")
                return data

        else:
            print("ERR: cannot load token/no valid key found.")
            return None
    except Exception as e:
        print(f"ERR: failed to load/decrypt token: {e}")
        return None

with open(path, "r") as file:
    token_data = json.load(file)

print("token expired?:", check_token_expired(token_data["expiry_time"]))

save_token_to_file(token_data, "C:\\Users\\ktmcw\\Desktop\\encrypted_token.json", key_file)

loaded_token = load_token_from_file("C:\\Users\\ktmcw\\Desktop\\encrypted_token.json", key_file)
if loaded_token:
    print("token:", loaded_token)
