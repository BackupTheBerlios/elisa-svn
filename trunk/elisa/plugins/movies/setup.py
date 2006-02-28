from setuptools import setup, find_packages

setup(
    name="ElisaMovies",
    version="0.0",
    description="""Movies plugin""",
    author="Phil",
    #install_requires = ["Cheetah >= 1.0"],
    packages=['movies_plugin'],
    entry_points="""
    [elisa.plugins]
    movies = movies_plugin.movies:MoviesTreePlugin
    """)
