import hashlib
import binascii
from cp_otp import strxor


try:
    from Crypto.Cipher import AES

except ImportError:  # Damn you, OS X
    import crypto, sys
    sys.modules['Crypto'] = crypto
    from crypto.Cipher import AES


PADDING = b'\x42'
BLOCK_SIZE = 16
KEY_LENGTH = 32
STREAM_LENGTH = 3


def _ensure_bytes_key(key, length):
    if type(key) is str:
        key = bytes(key, encoding='utf-8')
    key += bytes(length)
    return key[:length]


def _pad_data(data, block_size):
    padding_required = block_size - (len(data) % block_size)
    data += PADDING * padding_required
    assert len(data) % block_size == 0
    return data


def _unpad_data(data, block_size):
    return data.rstrip(PADDING)   # TODO Repeat single character by single character until % block_size == 0.
                                  #      Test if it is working by using a image of PADDING_SIZE bytes.


def _keystream(key_length, seed):
    last_key = seed
    key_length *= 2  # Hex characters that make up a byte
    while True:
        next_key = ""
        while len(next_key) < key_length:
            next_key += hashlib.sha1((next_key if next_key else last_key).encode('utf-8')).hexdigest()
        yield binascii.unhexlify(next_key[:key_length])
        last_key = next_key


def get_ecb_encrypter(key, block_size=BLOCK_SIZE, key_length=KEY_LENGTH):
    key = _ensure_bytes_key(key, length=key_length)

    def encrypter(x):
        x = _pad_data(x, block_size=block_size)
        cipher = AES.AESCipher(key[:32], AES.MODE_ECB)
        return cipher.encrypt(x)

    return encrypter


def get_ecb_decrypter(key, block_size=BLOCK_SIZE, key_length=KEY_LENGTH):
    key = _ensure_bytes_key(key, length=key_length)

    def decrypter(x):
        cipher = AES.AESCipher(key[:32], AES.MODE_ECB)
        x = _pad_data(x, block_size=block_size)  # This is a hack, and will loose the last pixels.
        x = cipher.decrypt(x)
        x = _unpad_data(x, block_size=block_size)
        return x
    
    return decrypter


def get_stream_cipher(seed, size=STREAM_LENGTH):
    def encrypter(x):
        y = b''
        for data_start_index, key in zip(range(0, len(x), size),
                                         _keystream(key_length=size, seed=seed)):
            y += strxor(x[data_start_index:data_start_index + size], key)
        return y
    return encrypter

