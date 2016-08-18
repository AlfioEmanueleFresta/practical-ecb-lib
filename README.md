## Python C Extension for the ECB Encryption Practical

This library provides some utility functions that can be used to operate on images
as a single byte literal -- where each pixel is represented as three bytes (R, G, B).

It allows to define a simple function which operates on a string of bytes and apply
the function to the pixels body of the image, generating a valid image as output.

The purpose of this library is to allow to demonstrate visually the effects of different
encryption methods on images. For this reason, this library also provides functions to
encrypt the body using a few different encryption techniques.



This is part of the [Cyber Security Practicals](https://cs.york.ac.uk/cyber-practicals/).

Copyright (c)2016 Alfio Emanuele Fresta


### Requirements

* Python 3,
* PIP,
* Linux, OS X or (probably) Windows.


### Install

```bash
sudo pip3 install git+https://github.com/AlfioEmanueleFresta/practical-ecb-lib.git
```

or,

```bash
git clone https://github.com/AlfioEmanueleFresta/practical-ecb-lib.git
cd practical-ecb-lib/
sudo pip3 install ./
```

### Test

```bash
cd practical-ecb-lib/
python3 tests.py
```

### Limitations

* **This library is for demonstration purposes only.**
  The encryption function is free to return a different number of bytes (e.g. ECB encryption, which
  requires padding to a multiple of 16 bytes). When saved, the extra padding bytes will be truncated
  to make the resulting output a valid image. The decrypter therefore needs to apply padding again, 
  and the union of these two factors *will* cause the last pixels of the image to be corrupted.
  
* **This library is slow on large images.**
  Currently this library uses PIL's `Image.putdata` which writes the image pixel by pixel,
  and is as slow as it can possibly get. May be fixed at a later time.
  
* **The stream cipher implementation is weak.**
  Again, demonstration purposes only. The implementation in the library simply uses
  a one-way hashing function to *imitate* the behaviour of a stream cipher. Its only
  purpose is to produce an image which looks like one encrypted using a proper stream 
  cipher implementation.


## Usage

This is the original image used for the examples:

![Original image](https://raw.githubusercontent.com/AlfioEmanueleFresta/practical-ecb-lib/master/examples/tux.png "Original Image")

`examples/tux.png`


### Stream cipher encryption

```python
from cp_ecb import encrypt_image_file, decrypt_image_file,\
                   get_stream_cipher


cipher = get_stream_cipher(seed="This is my seed")

encrypt_image_file("examples/tux.png", cipher, "otp-encrypted.png")
decrypt_image_file("otp-encrypted.png", cipher, "ecb-decrypter.png")
```

![Stream cipher](https://raw.githubusercontent.com/AlfioEmanueleFresta/practical-ecb-lib/master/examples/otp.png "Stream cipher image")

`examples/otp.png`


### ECB encryption

```python
from cp_ecb import encrypt_image_file, decrypt_image_file,\
                   get_ecb_encrypter, get_ecb_decrypter

key = "This is my secret key."

encrypter = get_ecb_encrypter(key)
decrypter = get_ecb_decrypter(key)

encrypt_image_file("examples/tux.png", encrypter, "ecb-encrypted.png")
decrypt_image_file("ecb-encrypted.png", decrypter, "ecb-decrypter.png")
```

![ECB encrypted image](https://raw.githubusercontent.com/AlfioEmanueleFresta/practical-ecb-lib/master/examples/ecb.png "ECB encrypted image")

`examples/ecb.png`


### Custom function (colours inverter)

```python
from cp_ecb import encrypt_image_file, decrypt_image_file


# Define an function which operates on byte literals
inverter = lambda image: bytes([0xff - pixel for pixel in image])  # Invert colours

encrypt_image_file("examples/tux.png", inverter, "inverted.png")
```

![Inverted colours image](https://raw.githubusercontent.com/AlfioEmanueleFresta/practical-ecb-lib/master/examples/inverted.png "Inverted colours image")

`examples/inverted.png`
