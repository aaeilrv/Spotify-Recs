from setuptools import setup, find_packages

requires = [
    'flask',
    'requests',
    'python-dotenv'
    'datetime',
]

setup(
    name='spotify-recs',
    version='0.1',
    description='get spotify recs',
    author='Valeria Vera & Luis García',
)

# python setup.py install