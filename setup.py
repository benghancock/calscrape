import setuptools

version = {}
with open("calscrape/version.py") as f:
    exec(f.read(), version)

with open("README.rst", "r") as readme:
    long_description = readme.read()

setuptools.setup(
    name="calscrape",
    version=version["__version__"],
    author="Ben Hancock",
    author_email="bghancock@vivaldi.net",
    description="Scrape and search federal court hearing data",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/elwha1/calscrape",
    packages=["calscrape"],
    package_dir={"calscrape": "calscrape"},
    package_data={"calscrape": ["*.ini"]},
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
