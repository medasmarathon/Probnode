from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
  long_description = fh.read()

setup(
    name="probnode",
    version="0.2.2",
    author="Duc Dang",
    author_email="vinhduc91@outlook.com",
    description="Probability expression library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/medasmarathon/Proba",
    project_urls={
        "Bug Tracker": "https://github.com/medasmarathon/Proba/issues",
        "Documentation": "https://github.com/medasmarathon/Probnode/wiki"
        },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers"
        ],
    packages=find_packages(exclude=['example*', '*constant*', 'sample*', '*test*']),
    python_requires=">=3.7",
    install_requires=["pyfields"]
    )
