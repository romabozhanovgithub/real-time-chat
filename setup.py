from setuptools import setup, find_packages

from community import __version__

setup(
    name="community",
    version=__version__,
    description="Community API",
    author="Community",
    url="https://github.com/romabozhanovgithub/real-time-chat.git",
    packages=find_packages(),
    install_requires=[
        "aioboto3>=11.2.0",
        "mypy_boto3_dynamodb>=1.26.158"
    ],
    python_requires=">=3.10",
)
