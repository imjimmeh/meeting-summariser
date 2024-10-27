from setuptools import find_packages, setup

with open("requirements.txt") as f:
    install_requires = f.read().splitlines()

setup(
    name="meeting-summariser",
    version="0.1.9",
    packages=find_packages(),
    install_requires=install_requires,
    entry_points={
        "console_scripts": [
            "meetingsummariser=meetingsummariser.main:main",
        ],
    },
)
