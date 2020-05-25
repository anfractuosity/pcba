import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pcba", 
    version="0.0.1",
    author="anfractuosity",
    description="",
    python_requires='>=3.8',
    install_requires=['numpy>=1.16','matplotlib>=3.0'],
    scripts=['pcba']
)
