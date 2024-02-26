from setuptools import setup

setup(
    name="my-package",
    version="1.0.0",
    description="My package description",
    author="Atwood",
    author_email="hecw2016@gmail.com",
    packages=["package1", "package2"],
    install_requires=["some-dependency"],
    python_requires=">=3.6",
)