from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='windfreak',
    version='0.2.1',
    author='Christian Hahn',
    author_email='christianhahn09@gmail.com',
    description='Python package for Windfreak Technologies devices.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/christian-hahn/windfreak-python',
    packages=find_packages(exclude=['tests', 'examples']),
    install_requires=[
        'pyserial',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    license='MIT',
    python_requires='>=3',
)
