from setuptools import setup, find_packages

def parse_requirements(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file if line.strip() and not line.startswith("#")]

setup(
    name="pglogging",
    version="0.1",
    packages=find_packages(),
    install_requires=parse_requirements("requirements.txt"),
    description="A simple example Python package with a class",
    author="Marcus Oates",
    author_email="marcusjoates@gmail.com",
    url="https://github.com/yourusername/mypackage",
)
