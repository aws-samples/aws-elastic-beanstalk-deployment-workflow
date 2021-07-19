import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ebextensions_validator", 
    version="1.0.2",
    author="Michael Füllbier",
    author_email="fuellbie@amazon.com",
    description="A CLI tool to validate ebextensions configuration files against a allowlist",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.aws.dev/fuellbie/ebextensions-validator",
    packages=setuptools.find_packages(exclude=["tests"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "cfn-flip"
    ],
    tests_require=[
        'pytest',
        'pytest-cov'
    ],
    python_requires='>=3.8',
    entry_points={
        "console_scripts": ["ebextensions-validator=ebextensions_validator.main:main"]
    }
)
