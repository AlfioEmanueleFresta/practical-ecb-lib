from setuptools import setup
from os import path, listdir
from pip.req import parse_requirements


requirements = parse_requirements("%s/requirements.txt" % path.abspath(path.dirname(__file__)), session=False)
requirements = [str(ir.req) for ir in requirements]

setup(

    name='Image Body Encryption',
    version='1.0',
    author='Alfio E. Fresta',
    author_email='aef517@york.ac.uk',
    url="https://www.cs.york.ac.uk/cyber-practicals/",

    license='BSD New',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD New',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    packages=['cp_ecb'],
    package_dir={'cp_ecb': 'cp_ecb'},
)