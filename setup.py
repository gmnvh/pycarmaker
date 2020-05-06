import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pycarmaker",  # Replace with your own username
    version="0.0.1",
    author="Gustavo Muller Nunes",
    author_email="gustavo.vh@gmail.com",
    description="CarMaker Python Interface",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gmnvh/pycarmaker",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

)
