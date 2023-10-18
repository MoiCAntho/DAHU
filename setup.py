from setuptools import setup,find_packages


setup(
    name = "DAHU",
    version = "0.0.0.0.2.3",
    author = "Virgile Cheminot, Anthony Louvat-Segura",
    url = "https://github.com/MoiCAntho/DAHU",
    packages = find_packages(),
    install_requires = ["wheel>=0.41.2",
                        "cython>=3.0.4",
                        "git+https://gitlab.math.univ-paris-diderot.fr/han/giacpy@master"]
    description="Package de calcul formel (pour l'instant ;=) )",
    license="MIT",
    python_requires = ">=3.8",
    classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    ],
    )