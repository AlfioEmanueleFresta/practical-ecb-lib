## Python C Extension for the ECB Encryption Practical

Part of the [Cyber Security Practicals](https://cs.york.ac.uk/cyber-practicals/).

Copyright (c)2016 Alfio Emanuele Fresta

### Install

```bash
git clone https://github.com/AlfioEmanueleFresta/practical-ecb-lib.git
cd practical-ecb-lib/
sudo python3 setup.py build --force install
```

### Test

```bash
python3 tests.py
```


## Usage


### ECB encryption

```python
from cp_ecb import encrypt_image_file, decrypt_image_file,\
                   get_ecb_encrypter, get_ecb_decrypter

key = "This is my secret key."

encrypter = get_ecb_encrypter(key)
decrypter = get_ecb_decrypter(key)

# Encrypt the image.
encrypt_image_file("examples/tux.png", encrypter, "ecb-encrypted.png")
decrypt_image_file("ecb-encrypted.png", decrypter, "ecb-decrypter.png")
```


### Stream cipher encryption

```python
from cp_ecb import encrypt_image_file, decrypt_image_file,\
                   get_stream_cipher


cipher = get_stream_cipher(seed="This is my seed")

encrypt_image_file("examples/tux.png", cipher, "otp-encrypted.png")
decrypt_image_file("otp-encrypted.png", cipher, "ecb-decrypter.png")
```


### Custom function (colours inverter)

```python
from cp_ecb import encrypt_image_file, decrypt_image_file


# Define an encryption function which operates on byte literals
inverter = lambda image: bytes([0xff - pixel for pixel in image])  # Invert colours

encrypt_image_file("examples/tux.png", inverter, "inverted.png")
```