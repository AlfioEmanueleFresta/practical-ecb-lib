import unittest
from PIL import Image
from cp_ecb import load_image, encrypt_image, decrypt_image,\
                   get_ecb_encrypter, get_stream_cipher, encrypt_image_file,\
                   decrypt_image_file, get_ecb_decrypter


SOURCE_IMAGE_TUX = "examples/tux.png"
SOURCE_IMAGE_42 = "examples/42.png"

TARGET_DIFFERENCE_TUX = 4
TARGET_DIFFERENCE_42 = 4


def _get_images_difference(file_a, file_b):
    """
    Gets the number of different pixels between two images.
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
    different = 0
    for a, b in zip(file_a, file_b):
        different += sum([0 if j == k else 1 for j, k in zip(a, b)])
    return different / 3


class ECBTests(unittest.TestCase):

    def test_sanity(self):
        invert = lambda x: bytes([255 - y for y in x])
        image = load_image(SOURCE_IMAGE_TUX)
        original = image.b
        inverted = encrypt_image(image, invert)
        self.assertTrue(original != inverted.b)
        inverted = decrypt_image(image, invert)
        self.assertTrue(original == inverted.b)

        key = "My secret key"
        encrypter = get_ecb_encrypter(key)
        encrypt_image_file(SOURCE_IMAGE_TUX, encrypter, "examples/ecb.png")

        # Decrypt correctly
        decrypter = get_ecb_decrypter(key)
        decrypt_image_file("examples/ecb.png", decrypter, "examples/ecb-d.png")
        difference = _get_images_difference(SOURCE_IMAGE_TUX, "examples/ecb-d.png")
        self.assertTrue(difference <= TARGET_DIFFERENCE_TUX)

        # Use a wrong decrypter
        decrypter = get_ecb_decrypter("Some other key")
        decrypt_image_file("examples/ecb.png", decrypter, "examples/ecb-x.png")
        difference = _get_images_difference(SOURCE_IMAGE_TUX, "examples/ecb-x.png")
        self.assertTrue(difference > TARGET_DIFFERENCE_TUX)

    def test_ecb_padding(self):
        key = "My secret key"
        encrypter = get_ecb_encrypter(key)
        encrypt_image_file(SOURCE_IMAGE_42, encrypter, "examples/ecb-42.png")
        decrypter = get_ecb_decrypter(key)
        decrypt_image_file("examples/ecb-42.png", decrypter, "examples/ecb-42-d.png")
        difference = _get_images_difference(SOURCE_IMAGE_42, "examples/ecb-42-d.png")
        self.assertTrue(difference <= TARGET_DIFFERENCE_42)

    def test_make_otp(self):
        cipher = get_stream_cipher(seed="My secret seed")
        encrypt_image_file(SOURCE_IMAGE_TUX, cipher, "examples/otp.png")

        # Decrypt correctly
        decrypt_image_file("examples/otp.png", cipher, "examples/otp-d.png")
        difference = _get_images_difference(SOURCE_IMAGE_TUX, "examples/otp-d.png")
        self.assertTrue(difference <= TARGET_DIFFERENCE_TUX)

        # Use a wrong cipher to decrypt
        cipher = get_stream_cipher(seed="Not my secret seed")
        decrypt_image_file("examples/otp.png", cipher, "examples/otp-d.png")
        difference = _get_images_difference(SOURCE_IMAGE_TUX, "examples/otp-d.png")
        self.assertTrue(difference > TARGET_DIFFERENCE_TUX)

    def test_make_invert(self):
        inverter = lambda image: bytes([0xff - pixel for pixel in image])
        encrypt_image_file(SOURCE_IMAGE_TUX, inverter, "examples/inverted.png")
        decrypt_image_file("examples/inverted.png", inverter, "examples/inverted-d.png")
        difference = _get_images_difference(SOURCE_IMAGE_TUX, "examples/inverted-d.png")
        self.assertTrue(difference == 0.00)

    def test_make_shorter_invert(self):
        inverter = lambda image: [0xff - pixel for pixel in image]
        encrypt_image_file(SOURCE_IMAGE_TUX, inverter, "examples/inverted.png")
        decrypt_image_file("examples/inverted.png", inverter, "examples/inverted-d.png")
        difference = _get_images_difference(SOURCE_IMAGE_TUX, "examples/inverted-d.png")
        self.assertTrue(difference == 0.00)

    def test_make_caesar(self):
        offset = 128
        caesar_encrypter = lambda image: bytes([(pixel + offset) % 0xff for pixel in image])
        caesar_decrypter = lambda image: bytes([(pixel - offset) % 0xff for pixel in image])
        encrypt_image_file(SOURCE_IMAGE_TUX, caesar_encrypter, "examples/caesar.png")
        decrypt_image_file("examples/caesar.png", caesar_decrypter, "examples/caesar-d.png")
        difference = _get_images_difference(SOURCE_IMAGE_TUX, "examples/caesar-d.png")
        self.assertTrue(difference == 0.00)


if __name__ == '__main__':
    unittest.main()

