from setuptools import setup

with open("./README.md", "r") as f:
    long_desc = f.read()

setup(
    name="iotadb",
    version="0.0.13",
    description="Minimal implementation of a local embedding database",
    packages=["iotadb"],
    long_description=long_desc,
    long_description_content_type="text/markdown",
    url="https://github.com/timothyckl/iota",
    author="timothyckl",
    author_email="timothy.ckl@outlook.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Operating System :: OS Independent",
    ],
    install_requires=["numpy", "sentence-transformers"],
    extras_require={"dev": ["pytest", "twine"]},
    python_requires=">=3.8",
)
