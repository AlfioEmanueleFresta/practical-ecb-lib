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


def read_image(input_file, encrypted=False, silent=False):

    if not silent:
        print("Reading image %s..." % input_file, end=" ", flush=True)

    image_file = Image.open(input_file)
    image = image_file.convert('RGB')

    image_size = image.size

    image_b = b''
    for y in range(image_size[1]):
        for x in range(image_size[0]):
            r, g, b = image.getpixel((x, y))
            image_b += bytes([r, g, b])

    if not silent:
        print("OK")

    image_file.close()

    return InMemoryImage(w=image_size[0], h=image_size[1],
                         c=3, b=image_b, encrypted=encrypted)


def write_image(image, output_file, silent=False):

    if not silent:
        print("Writing image to file %s..." % output_file, end=" ", flush=True)

    output = Image.new("RGB", (image.w, image.h))
    maxlen = len(image.b) - (len(image.b) % image.c)
    data = tuple(tuple(image.b[i:i + image.c]) for i in range(0, maxlen, image.c))
    data = data[:(image.w * image.h)]
    output.putdata(data)
    output.save(output_file)

    if not silent:
        print("OK")


def _crypt_image(encrypt, input, function, silent=False):

    if type(input) is not InMemoryImage:
        raise ValueError("You need to pass this function a valid InMemoryImage object.")

    if encrypt and input.encrypted:
        raise ValueError("The input image is already encrypted.")

    elif (not encrypt) and (not input.encrypted):
        raise ValueError("The input image is not flagged as encrypted and can't be decrypted.")

    if not silent:
        print("%s image..." % ("Encrypting" if encrypt else "Decrypting"), end=" ", flush=True)

    input.b = function(input.b)

    # Allow return list of ordinals
    if type(input.b) is list:
        input.b = bytes(input.b)

    input.encrypted = encrypt

    if not silent:
        print("OK")

    return input


def encrypt_image(input, function, silent=False):
    return _crypt_image(encrypt=True, input=input, function=function, silent=silent)


def decrypt_image(input, function, silent=False):
    return _crypt_image(encrypt=False, input=input, function=function, silent=silent)


def encrypt_image_file(input_file, function, output_file, silent=False):
    image = read_image(input_file, silent=silent)
    image = encrypt_image(image, function, silent=silent)
    write_image(image, output_file, silent=silent)


def decrypt_image_file(input_file, function, output_file, silent=False):
    image = read_image(input_file, encrypted=True, silent=silent)
    image = decrypt_image(image, function, silent=silent)
    write_image(image, output_file, silent=silent)
