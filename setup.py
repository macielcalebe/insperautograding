import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="insperautograder",
    version="0.4.0",
    author="Maciel Calebe Vidal",
    author_email="macielcv@insper.edu.br",
    description="Autograding for Insper Students",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/macielcalebe/insperautograding",
    project_urls={
        "Bug Tracker": "https://github.com/macielcalebe/insperautograding/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPL v2",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
    install_requires=["python-dotenv", "requests", "ipython", "ipywidgets<=7.8.5"],
)
