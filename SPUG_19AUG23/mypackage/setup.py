import os.path
from setuptools import setup, Extension

setup(
    name="mypackage",
    package_dir={"": "src"},
    ext_modules=[
        Extension(
            name="mypackage.hello_world",
            sources=[os.path.join("src", "mypackage", "extension.c")]
        )
    ]
)
