from setuptools import setup, find_packages

setup(
    name="ElisaDataFS",
    version="0.0",
    description="""Data filesystem access plugin""",
    author="Phil",
    #install_requires = ["Cheetah >= 1.0"],
    packages=['data_fs_plugin'],
    entry_points="""
    [elisa.plugins.data]
    fs = data_fs_plugin.fs:DataFSPlugin
    """)
