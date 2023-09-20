import os.path
from setuptools import setup, Extension

setup(
    name="mystack",
    package_dir={"": "src"},
    ext_modules=[
        Extension(
            name="mystack.stack",
            sources=[os.path.join("src", "mystack", "stack.c")]
        )
    ]
)
