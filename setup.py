from setuptools import setup

from terraflow.version import __version__

setup(
    name="terraflow",
    version=__version__,
    py_modules=["terraflow"],
    install_requires=[
        "Click",
    ],
    entry_points="""
        [console_scripts]
        terraflow=terraflow:terraflow
    """,
)
