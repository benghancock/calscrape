import setuptools

with open("README.rst", "r") as readme:
    long_description = readme.read()

setuptools.setup(
    name="calscrape-elwha1",
    version="2.0.1-dev",
    author="Ben Hancock",
    author_email="bghancock@vivaldi.net",
    description="scrape and search federal court hearing data",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/elwha1/calscrape",
    packages=setuptools.find_packages(),
    entry_points={
        "console_scripts": ["calscrape=calscrape.calscrape:main"]
    },
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: POSIX"
    ],
    python_requires=">=3.6"
)
