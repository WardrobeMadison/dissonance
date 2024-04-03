from setuptools import find_packages, setup

setup(
    name="dissonance",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "scipy",
        "scikit-learn",
        "pandas",
        "h5py",
        "tables",
        "numpy",
        "plotly",
        "matplotlib",
        "PyQt5",
        "jupyter",
        "ipykernel",
    ],
)
