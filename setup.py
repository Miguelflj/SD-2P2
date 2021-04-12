from setuptools import setup

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
   name='Trab1-SD',
   version='1.0',
   description='Estudo de caso RMI',
   license="MIT",
   long_description=long_description,
   author='Miguel Freitas',
   author_email='miguelfljunior@gmail.com',
   url="https://github.com/Miguelflj/SD-2P2",
   packages=['os','sys','threading','datetime'],  #same as name
   install_requires=['Pyro5'], #external packages as dependencies
)