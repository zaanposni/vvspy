from setuptools import setup, find_packages

with open("readme.md", "r") as fh:
    long_description = fh.read()

setup(
    name="vvspy",
    version="2.0.0",
    license="MIT",
    description="API Wrapper for VVS (Verkehrsverbund Stuttgart)",
    author="zaanposni",
    author_email="vvspy@zaanposni.com",
    url="https://github.com/zaanposni/vvspy",
    keywords=["vvs", "api", "stuttgart", "wrapper", "json", "rest", "efa", "python"],
    packages=find_packages(exclude=["*tests"]),
    package_data={"vvspy": ["vvspy/*"]},
    python_requires=">=3.6",
    install_requires=[
        "requests",
        "typing",
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
)
