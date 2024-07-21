import hashlib

def generate_name(name):
    name = name + 'xuanloc'
    name_bytes = name.encode('utf-8')
    hash_object = hashlib.sha256(name_bytes)
    hex_dig = hash_object.hexdigest()
    return hex_dig