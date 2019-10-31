# test runner file
import unittest
import os

if __name__ == "__main__":
    loader = unittest.TestLoader()
    start_dir = os.path.join(os.path.curdir, "tests")
    suite = loader.discover(start_dir)
    runner = unittest.TextTestRunner()
    runner.run(suite)
