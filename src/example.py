# Functional Modules
from math import e, pi
import numpy as np

# Verification Modules
import unittest as ut


# Main
def myfunction(A: float, B:str, C:int) -> list:
    """
    This function is useless
    :param A: a float
    :param B: a string
    :param C: an integer
    :return: list
    """
    return [A, B, C]


class Example(object):

    def __init__(self):
        self.__example = True   # The __ before a variable name indicates its a hidden variable.
                                # Use this for encapsulation purposes

    def get_example(self) -> bool:      # Indicate the expected output type(s)
        return self.__example

    def set_example(self, ex: bool):    # Indicate the expected input type(s)
        self.__example = ex


if __name__ == "__main__":              # Code will only be executed if this is the main file being run
                                        # Code outside this if statement will also be run in this file is imported
                                        # into another script

    class ExampleTestCases(ut.TestCase):

        def setUp(self):
            """
            Will execute before every test being executed
            """
            self.example = Example()

        def tearDown(self):
            """
            Will execute after every test being executed
            """
            pass

        def test_example(self):
            """
            Simple test being run
            """
            self.assertEqual(self.example.get_example(), True)

    def run_TestCases():
        suite = ut.TestLoader().loadTestsFromTestCase(ExampleTestCases)
        ut.TextTestRunner(verbosity=2).run(suite)


    run_TestCases()
