from setuptools import setup,find_packages
import setuptools_scm


setup(
    name = "DAHU",
    version = "0.0.0.0.2.4",
    author = "Virgile Cheminot, Anthony Louvat-Segura",
    url = "https://github.com/MoiCAntho/DAHU",
    packages = find_packages(),
    install_requires = ["wheel>=0.40.0",
                        "cython>=3.0.1"
                        ],
    dependency_links=["git+https://gitlab.math.univ-paris-diderot.fr/han/giacpy@master"
    ],
    description="Package de calcul formel (pour l'instant ;=) )",
    license="MIT",
    python_requires = ">=3.8",
    classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    ],
    use_scm={"version_scheme": "guess-next-dev", "local_scheme": "dirty-tag", "prefer_binary": True}
    )