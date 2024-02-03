from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='TopTrackPy',
    version='0.1-alpha',
    packages=find_packages(),
    install_requires=requirements,
    url='https://github.com/milano-slesarik/toptrackpy.git',
    author='Milan Slesarik',
    author_email='milslesarik@gmail.com'
)