import os
from setuptools import setup, find_packages
import pathlib


here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file

# Get install requires
requirements = f'{os.path.dirname(os.path.realpath(__file__))}/requirements.txt'

if os.path.isfile(requirements):
    with open(requirements) as f:
        install_requires = f.read().splitlines()

setup(
    name='K_Warp_2021',
    version='0.0.0',
    description='Pacote para extrair dados de medidas ARPES na UFMG',
    author='Clovis',
    author_email='clovisguerim@gmail.com',
    url='https://github.com/clovisguerim',
    packages=find_packages(exclude='docs'),
    install_requires=install_requires,
    data_files=[('requirements', ['requirements.txt'])]
)
