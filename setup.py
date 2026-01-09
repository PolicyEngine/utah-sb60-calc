from setuptools import setup, find_packages

setup(
    name="utah-sb60-calc",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "policyengine-us>=1.0.0",
        "policyengine-core>=3.0.0",
        "pandas>=2.0.0",
        "plotly>=5.0.0",
    ],
)
