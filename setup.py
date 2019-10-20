import os
import setuptools


# currentdir = os.getcwd()

with open("README.rst", "r", encoding="utf-8") as f:
    long_desc = f.read()

with open("LICENSE", "r", encoding="utf-8") as f:
    license_str = f.read()

setuptools.setup(
    name="edigital",
    version="0.1",
    author='Kaan Eraslan',
    python_requires='>=3.5.0',
    author_email="kaaneraslan@gmail.com",
    description="Digital Edition Suite using Authority Documents",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    license=license_str,
    url="https://github.com/D-K-E/digital-edition-suite",
    packages=setuptools.find_packages(
        exclude=["tests", "*.tests", "*.tests.*", "tests.*",
                 "docs", ".gitignore", "README.rst"]
    ),
    test_suite="tests",
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Creative Commons Attribution 4.0 International",
        "Operating System :: OS Independent",
    ],
)
