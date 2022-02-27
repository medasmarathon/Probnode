from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
  long_description = fh.read()

setup(
    name="probnode",
    version="0.1.0",
    author="Duc Dang",
    author_email="vinhduc91@outlook.com",
    description="Probability library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/medasmarathon/Proba",
    project_urls={
        "Bug Tracker": "https://github.com/medasmarathon/Proba/issues",
        },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        ],
    packages=find_packages(exclude=['example*', '*constant*', 'sample*', '*test*']),
    python_requires=">=3.6",
    install_requires=[]
    )
