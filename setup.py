import os

from setuptools import setup, find_packages

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

service_name = os.path.basename(os.getcwd())

setup(
    name=service_name,
    version="0.1.0",
    author="",
    author_email="",
    description="Backend service for AMA HØI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/oyvinyg/ama-hoi",
    packages=find_packages(),
    install_requires=[
        "boto3",
        "fastapi",
        "pydantic==1.8.2",
    ],
)
