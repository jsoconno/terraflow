from setuptools import setup

setup(
    name="terraflow",
    version="0.1.0",
    py_modules=["terraflow"],
    install_requires=[
        "Click",
    ],
    entry_points="""
        [console_scripts]
        terraflow=terraflow:terraflow
    """,
)
