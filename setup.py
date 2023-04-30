from setuptools import setup, find_packages
from pathlib import Path

# version
here = Path(__file__).absolute().parent
version_data = {}
with open(here.joinpath("musicrecolib", "__init__.py"), "r") as f:
    exec(f.read(), version_data)
version = version_data.get("__version__", "0.0.0")

install_requires = [
    'nbformat==5.1.3',
    'nbconvert==6.0.7',
    'ipykernel==6.4.1',
    'matplotlib==3.7.1', 
    'python-dotenv==0.19.1',
    'pandas',
    'numpy',
    'scikit-learn==1.2.2', 
    'polars==0.10.0',
    'pylab-sdk',  # Please check the library version
    'kneed==0.8.1',
    'pyspark==3.4.0', 
    'pyarrow==11.0.0', 
    'pytest==6.2.4',
    'pytest-xdist==2.3.0',
    'requests==2.26.0',
    'nbmake',  # Please check the library version
    'xgboost==1.4.2',
    'seaborn==0.11.1',
    'tensorflow',
    'tdqm',  # Please check the library version
    'pytest-timeout==1.4.2',
    'psycopg2'
]


setup(
    name="musicrecolib",
    version=version,
    install_requires=install_requires,
    package_dir={"musicrecolib": "musicrecolib"},
    python_requires=">=3.6, <3.11.1",
    packages=find_packages(where=".", exclude=["examples", "tests", "Deployment", "Extension", "Front-End", "Procfile", "heroku.yml", "requirements.txt"])
)
