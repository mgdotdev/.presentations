from setuptools import setup, find_packages

setup(
    name="api",
    version="0.0.1",
    license="MIT",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
)
