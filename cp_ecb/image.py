from PIL import Image


class InMemoryImage:
    """
    A very simple class to represent an image.
    """

    def __init__(self, w, h, c=3,
                 b=b'', encrypted=False):
        """
        Instantiate a new image.
        :param w: The width of the image (px).
        :param h: The height of the image (px).
        :param c: The number of colour channels of the image. Default is 3.
        :param b: A byte literal for the body of the image.
        :param encrypted: A flag to say whether the image is encrypted or not.
        """
        self.w = w
        self.h = h
        self.c = c
        self.b = b
        self.encrypted = encrypted

    def __repr__(self):
        return "<InMemoryImage(%s): channels=%d, width=%d, height=%d>" % (
            "encrypted" if self.encrypted else "unencrypted",
            self.c, self.w, self.h
        )


def load_image(input_file, encrypted=False):
    """
    Load an image file into memory as a InMemoryImage object.

    :param input_file: The file to load.
    :param encrypted: Whether to flag the file as an encrypted image or not.
    :return: An instantiated InMemoryImage object.
    """

    image_file = Image.open(input_file)
    image = image_file.convert('RGB')
    image_size = image.size

    image_b = b''
    for y in range(image_size[1]):
        for x in range(image_size[0]):
            r, g, b = image.getpixel((x, y))
            image_b += bytes([r, g, b])

    image_file.close()

    return InMemoryImage(w=image_size[0], h=image_size[1],
                         c=3, b=image_b, encrypted=encrypted)


def save_image(image, output_file):
    output = Image.new("RGB", (image.w, image.h))
    maxlen = len(image.b) - (len(image.b) % image.c)
    data = tuple(tuple(image.b[i:i + image.c]) for i in range(0, maxlen, image.c))
    data = data[:(image.w * image.h)]
    output.putdata(data)
    output.save(output_file)


def _crypt_image(encrypt, image, function):

    if type(image) is not InMemoryImage:
        raise ValueError("You need to pass this function a valid InMemoryImage object.")

    if encrypt and image.encrypted:
        raise ValueError("The input image is already encrypted.")

    elif (not encrypt) and (not image.encrypted):
        raise ValueError("The input image is not flagged as encrypted and can't be decrypted.")

    image.b = function(image.b)

    # Allow return list of ordinals
    if type(image.b) is list:
        image.b = bytes(image.b)

    image.encrypted = encrypt

    return image


def encrypt_image(image, function):
    """
    Encrypt the content of an InMemoryImage using a given function.
    :param image: The unencrypted InMemoryImage object.
    :param function: An encryption function which takes a single bytes literal and returns a single bytes literal.
    :return: An encrypted InMemoryImage object.
    """
    return _crypt_image(encrypt=True, image=image, function=function)


def decrypt_image(image, function):
    """
    Decrypt the content of an InMemoryImage using a given function.
    :param image: The encrypted InMemoryImage object.
    :param function: A decryption function which takes a single bytes literal and returns a single bytes literal.
    :return: An unencrypted InMemoryImage object.
    """
    return _crypt_image(encrypt=False, image=image, function=function)


def encrypt_image_file(input_file, function, output_file):
    """
    Loads an image file, encrypts its contents and saves it as another image file.
    :param input_file: The original unencrytped image file.
    :param function: The encryption function to use. This must take a single bytes literal and return a single bytes literal.
    :param output_file: The file name for the encrypted image.
    """
    image = load_image(input_file)
    image = encrypt_image(image, function)
    save_image(image, output_file)


def decrypt_image_file(input_file, function, output_file):
    """
    Loads an encrypted image file, decrypts its contents and saves it as another image file.
    :param input_file: The encrypted image file.
    :param function: The decryption function to use. This must take a single bytes literal and return a single bytes literal.
    :param output_file: The file name for the decrypted image.
    """
    image = load_image(input_file, encrypted=True)
    image = decrypt_image(image, function)
    save_image(image, output_file)
