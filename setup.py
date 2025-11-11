from setuptools import setup, find_packages

setup(
    name="triass-tfec",
    version="3.1.0",
    packages=find_packages(),
    install_requires=[
        "zstandard>=0.21.0",
    ],
    extras_require={
        "test": ["pytest>=7.4.0", "pytest-cov>=4.1.0"],
    },
    entry_points={
        "console_scripts": [
            "tfec=triass_tfec.cli.main:main",
        ],
    },
    author="Syntriass Labs",
    author_email="dev@syntriass.org",
    description="Certifiable lossless compression with Zstandard fallback and EBTA receipts",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/syntriass-labs/tfec",
    license="MIT",
    python_requires=">=3.8",
)
