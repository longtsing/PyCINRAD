from os.path import join
from setuptools import find_packages, setup

data_pth = join("cinrad", "data")

setup(
    name="cinrad",
    version="1.9.3",
    description="Decode CINRAD radar data and visualize",
    long_description="Decode CINRAD radar data and visualize",
    license="GPL Licence",
    author="PyCINRAD Developers",
    author_email="dpy274555447@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    platforms=["Windows", "Linux", "MacOS"],
    python_requires=">=3.9",
    install_requires=[
        "numpy",
        "metpy>=0.8",
        "cartopy>=0.15",
        "pyshp!=2.0.0, !=2.0.1",
        "matplotlib>=2.2",
        "vanadis",
        "cinrad_data>=0.1"
    ],
    package_dir={"cinrad": "cinrad"},
    package_data={"cinrad": [
        "data/*.*",
        "data/*/*.*"
    ]},
    scripts=[],
)
