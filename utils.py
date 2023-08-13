import hashlib

def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()


def is_password_match(entered_password, stored_hash):
    # Calculate the MD5 hash of the entered_password
    entered_hash = hashlib.md5(entered_password.encode()).hexdigest()
    # Compare the entered hash with the stored hash
    return entered_hash == stored_hash