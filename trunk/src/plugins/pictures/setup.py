from setuptools import setup, find_packages

setup(
    name="ElisaPictures",
    version="0.0",
    description="""Pictures plugin""",
    author="Phil",
    #install_requires = ["Cheetah >= 1.0"],
    packages=['pictures_plugin'],
    entry_points="""
    [elisa.plugins]
    pictures = pictures_plugin.pictures:PicturesPluginTree
    """)
