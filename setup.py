import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tddish",
    version="1.0.0",
    author="justcli",
    author_email="pandey.justcli@fastmail.com",
    description="A tool for TDD based Test-While-Coding experience",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/justcli/ttdish",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={  # Optional
        'console_scripts': [
            'tddish=tddish:main',
        ],
    },   python_requires='>=3.6',
)
