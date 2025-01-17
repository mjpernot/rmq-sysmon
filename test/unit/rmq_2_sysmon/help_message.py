# Classification (U)

"""Program:  help_message.py

    Description:  Unit testing of help_message in rmq_2_sysmon.py.

    Usage:
        test/unit/rmq_2_sysmon/help_message.py

    Arguments:

"""

# Libraries and Global Variables

# Standard
import sys
import os
import unittest

# Local
sys.path.append(os.getcwd())
import rmq_2_sysmon                             # pylint:disable=E0401,C0413
import lib.gen_libs as gen_libs             # pylint:disable=E0401,C0413,R0402
import version                                  # pylint:disable=E0401,C0413

__version__ = version.__version__


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        test_help_message

    """

    def test_help_message(self):

        """Function:  test_help_message

        Description:  Test help_message function.

        Arguments:

        """

        with gen_libs.no_std_out():
            self.assertFalse(rmq_2_sysmon.help_message())


if __name__ == "__main__":
    unittest.main()
