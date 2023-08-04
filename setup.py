from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="citrusdb",
    version="0.5.2",
    author="Debabrata Mondal",
    author_email="debabrata.js@protonmail.com",
    description="(distributed) vector database",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/0xDebabrata/citrus",
    packages=(
        find_packages(
            exclude=["demo"]
        ) +
        ["citrusdb.db.index", "citrusdb.db.sqlite", "citrusdb.db.postgres"]
    ),
    include_package_data=True,
    install_requires=[
        "numpy",
        "hnswlib",
        "openai",
        "psycopg[c]",
        "psycopg[pool]"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
