from setuptools import setup, find_packages  # Import the necessary functions from setuptools
from pathlib import Path  # Import the Path class from the pathlib module

# version
here = Path(__file__).absolute().parent  # Get the absolute path of the current file's parent directory
version_data = {}
with open(here.joinpath("musicrecolib", "__init__.py"), "r") as f:
    exec(f.read(), version_data)  # Read the "__init__.py" file of the "musicrecolib" package and execute its contents
version = version_data.get("__version__", "0.0.0")  # Get the "__version__" attribute from the executed code, defaulting to "0.0.0" if not found

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
    name="musicrecolib",  # Name of the package
    version=version,  # Version of the package
    install_requires=install_requires,  # List of required dependencies for the package
    package_dir={"musicrecolib": "musicrecolib"},  # Specify the directory structure of the package
    python_requires=">=3.6, <3.11.1",  # Specify the supported Python versions
    packages=find_packages(where=".", exclude=["examples", "tests"])  # Find all packages in the current directory, excluding "examples" and "tests"
)
