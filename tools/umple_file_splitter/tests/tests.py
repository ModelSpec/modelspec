import unittest
import tempfile
import os
import shutil
from pathlib import Path

from ..umple_file_splitter import split_umple_python_source_file


class TestUmpleFileSplitter(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(__file__).parent
        self.resources_dir = self.test_dir / "resources"
        self.temp_output_dir = None


    def tearDown(self):
        if self.temp_output_dir and os.path.exists(self.temp_output_dir):
            shutil.rmtree(self.temp_output_dir)
            print(f"Deleted '{self.temp_output_dir}'")


    def test_splitting_umple_generated_code(self):
        """
        Test splitting a valid umple generated python file into its components.
        "./resources/foobar.py" contains two classes, Foo and Bar. Additionally, an "__init__.py" file should be created to facilitate imports.
        """
        # Arrange: given foobar.py is in resources and is valid
        self.temp_output_dir = tempfile.mkdtemp()
        input_file = self.resources_dir / "foobar.py"

        # Act: when we split foobar.py
        split_umple_python_source_file(str(input_file), self.temp_output_dir)
        
        # Assert: then the expected files are created with the correct content
        # assert the expected files exist
        expected_files = { "Foo.py", "Bar.py", "__init__.py" }
        for filename in expected_files:
            self.assert_file_exists_and_has_the_expected_content(filename)
        # assert no other files were created
        created_files = os.listdir(self.temp_output_dir)
        self.assertEqual(set(created_files), expected_files, f"Expected files {expected_files} but found {set(created_files)}")


    def assert_file_exists_and_has_the_expected_content(self, filename):
        expected_file_path = os.path.join(self.resources_dir, filename)
        actual_file_path = os.path.join(self.temp_output_dir, filename)

        # assert actual file exists
        self.assertTrue(os.path.exists(actual_file_path),f"Expect {filename} to be created, which it was not")

        # compare line by line
        with open(expected_file_path, 'r', encoding='utf-8') as expected_file:
            with open(actual_file_path, 'r', encoding='utf-8') as actual_file:
                for i, expected_line in enumerate(expected_file):
                    actual_line = actual_file.readline()

                    # assert content matches
                    self.assertEqual(expected_line, actual_line,
                        f"Mismatch in {filename} at line {i+1}:\nExpected: {expected_line}\nActual:   {actual_line}")


if __name__ == '__main__':
    unittest.main()
