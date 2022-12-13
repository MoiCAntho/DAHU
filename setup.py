from setuptools import setup,find_packages

#A finir

setup(
    name = "DAHU",
    version = "0.1.0",
    author = "Virgile Cheminot, Anthony Louvat-Segura",
    url = "https://github.com/MoiCAntho/DAHU",
    packages = find_packages(),
    install_requires = ["giacpy"]
    )