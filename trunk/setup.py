from setuptools import setup, find_packages

"""
TODO:

- complete the setup() parameters
- handle plugins building too ?

"""

packages  = find_packages()

setup(
    name="Elisa",
    version="0.0.1",
    description="""This is a MediaBox""",
    author="Foo",
    install_requires = ["ConfigObj >= 4.2", "Pygame >= 1.7",
                        
                        ],
    packages=packages)
