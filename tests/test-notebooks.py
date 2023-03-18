# Python file with code to test the basic functionality of all the notebooks in the repository

import os
import sys
import unittest
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor

class TestNotebooks(unittest.TestCase):
    def test_notebooks(self):
        # Get the list of notebooks in any part of the repository
        notebooks = [os.path.join(root, name)
                        for root, dirs, files in os.walk(".") for name in files
                        if name.endswith(".ipynb")]
        # Loop through the notebooks
        for notebook in notebooks:
            # Open the notebook
            with open(notebook) as f:
                nb = nbformat.read(f, as_version=4)
            # Execute the notebook and print which one is being executed
            print("Testing notebook: " + notebook)
            ep = ExecutePreprocessor(timeout=600, kernel_name='python 3.10')
            ep.preprocess(nb, {'metadata': {'path': '.'}})
            # Check for errors
            errors = [output for cell in nb.cells if "outputs" in cell for output in cell["outputs"] if output.output_type == "error"]
            self.assertEqual(errors, [])

if __name__ == '__main__':
    unittest.main()

