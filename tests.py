import unittest
import statistics
from PIL import Image
from cp_ecb import read_image, encrypt_image, decrypt_image,\
                   get_ecb_encrypter, get_stream_cipher, encrypt_image_file,\
                   decrypt_image_file, get_ecb_decrypter


SOURCE_IMAGE = "examples/tux.png"
TARGET_DIFFERENCE = 0.00005


def _get_images_difference(file_a, file_b):
    """
    Gets the average pixel value difference between two images
     of the same size.
    :param file_a: Filename A.
    :param file_b: Filename B.
    :return: A value between 0 and 1.
    """
    file_a = Image.open(file_a)
    file_a = file_a.convert("RGB")
    file_b = Image.open(file_b)
    file_b = file_b.convert("RGB")
    file_a = list(file_a.getdata())
    file_b = list(file_b.getdata())
    if len(file_a) != len(file_b):
        raise ValueError("Images have different size.")
    length = len(file_a)
    total = 0
    for a, b in zip(file_a, file_b):
        difference = statistics.mean([abs(j - k) / 255 for j, k in zip(a, b)])
        total += (difference / length)
    return total


class ECBTests(unittest.TestCase):

    def test_sanity(self):
        invert = lambda x: bytes([255 - y for y in x])
        image = read_image(SOURCE_IMAGE, silent=True)
        original = image.b
        inverted = encrypt_image(image, invert, silent=True)
        self.assertTrue(original != inverted.b)
        inverted = decrypt_image(image, invert, silent=True)
        self.assertTrue(original == inverted.b)

    def test_make_ecb(self):
        key = "My secret key"
        encrypter = get_ecb_encrypter(key)
        encrypt_image_file(SOURCE_IMAGE, encrypter, "examples/ecb.png", silent=True)

        # Decrypt correctly
        decrypter = get_ecb_decrypter(key)
        decrypt_image_file("examples/ecb.png", decrypter, "examples/ecb-d.png", silent=True)
        difference = _get_images_difference(SOURCE_IMAGE, "examples/ecb-d.png")
        self.assertTrue(difference <= TARGET_DIFFERENCE)

        # Use a wrong decrypter
        decrypter = get_ecb_decrypter("Some other key")
        decrypt_image_file("examples/ecb.png", decrypter, "examples/ecb-x.png", silent=True)
        difference = _get_images_difference(SOURCE_IMAGE, "examples/ecb-x.png")
        self.assertTrue(difference > TARGET_DIFFERENCE)

    def test_make_otp(self):
        cipher = get_stream_cipher(seed="My secret seed")
        encrypt_image_file(SOURCE_IMAGE, cipher, "examples/otp.png", silent=True)

        # Decrypt correctly
        decrypt_image_file("examples/otp.png", cipher, "examples/otp-d.png", silent=True)
        difference = _get_images_difference(SOURCE_IMAGE, "examples/otp-d.png")
        self.assertTrue(difference <= TARGET_DIFFERENCE)

        # Use a wrong cipher to decrypt
        cipher = get_stream_cipher(seed="Not my secret seed")
        decrypt_image_file("examples/otp.png", cipher, "examples/otp-d.png", silent=True)
        difference = _get_images_difference(SOURCE_IMAGE, "examples/otp-d.png")
        self.assertTrue(difference > TARGET_DIFFERENCE)

    def test_make_invert(self):
        inverter = lambda image: bytes([0xff - pixel for pixel in image])
        encrypt_image_file(SOURCE_IMAGE, inverter, "examples/inverted.png", silent=True)
        decrypt_image_file("examples/inverted.png", inverter, "examples/inverted-d.png", silent=True)
        difference = _get_images_difference(SOURCE_IMAGE, "examples/inverted-d.png")
        self.assertTrue(difference == 0.00)


if __name__ == '__main__':
    unittest.main()

