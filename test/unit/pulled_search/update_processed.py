# Classification (U)

"""Program:  update_processed.py

    Description:  Unit testing of update_processed in pulled_search.py.

    Usage:
        test/unit/pulled_search/update_processed.py

    Arguments:

"""

# Libraries and Global Variables

# Standard
import sys
import os
import shutil
import unittest
import mock

# Local
sys.path.append(os.getcwd())
import pulled_search
import version

__version__ = version.__version__


def file_to_list(fname):

    """Function:  file_to_list

    Description:  Read file into a list.

    Arguments:
        (input) fname -> Name of file
        (output) filelist -> List of file entries

    """

    with open(fname) as fhdr:
        filelist = fhdr.readlines()
        filelist = [line.rstrip() for line in filelist]

    return filelist


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_add_no_names
        test_add_multiple_names
        test_add_single_name
        test_update_existing_file
        test_create_new_file2
        test_create_new_file
        tearDown

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.basepath = "test/unit/pulled_search/testfiles"
        self.basepath2 = "test/unit/pulled_search/tmp"
        self.basefile = "test_update_processed.txt"
        self.fname = os.path.join(self.basepath2, self.basefile)
        self.fname2 = os.path.join(
            self.basepath2, "test_update_processed2.txt")
        f_name = "/path/file1"
        f_name2 = "/path/file2"
        self.file_dict = {"file1": f_name}
        self.file_dict2 = {"file1": f_name, "file2": f_name2}
        self.results = [f_name]
        self.results2 = [f_name, f_name2]
        self.results3 = [f_name, f_name2]

    @mock.patch("pulled_search.gen_class.Logger")
    def test_add_no_names(self, mock_log):

        """Function:  test_add_no_names

        Description:  Test with add no names to file.

        Arguments:

        """

        mock_log.return_value = True

        pulled_search.update_processed(mock_log, self.fname2, {})

        self.assertEqual(file_to_list(self.fname2), [])

    @mock.patch("pulled_search.gen_class.Logger")
    def test_add_multiple_names(self, mock_log):

        """Function:  test_add_multiple_names

        Description:  Test with add multiple names to file.

        Arguments:

        """

        mock_log.return_value = True

        pulled_search.update_processed(mock_log, self.fname2, self.file_dict2)
        data = file_to_list(self.fname2)
        data.sort()

        self.assertEqual(data, self.results3)

    @mock.patch("pulled_search.gen_class.Logger")
    def test_add_single_name(self, mock_log):

        """Function:  test_add_single_name

        Description:  Test with add single name to file.

        Arguments:

        """

        mock_log.return_value = True

        pulled_search.update_processed(mock_log, self.fname2, self.file_dict)

        self.assertEqual(file_to_list(self.fname2), self.results)

    @mock.patch("pulled_search.gen_class.Logger")
    def test_update_existing_file(self, mock_log):

        """Function:  test_update_existing_file

        Description:  Test with update to existing file.

        Arguments:

        """

        mock_log.return_value = True

        shutil.copy2(
            os.path.join(self.basepath, self.basefile), self.basepath2)
        pulled_search.update_processed(mock_log, self.fname, self.file_dict)
        data = file_to_list(self.fname)
        data.sort()

        self.assertEqual(data, self.results2)

    @mock.patch("pulled_search.gen_class.Logger")
    def test_create_new_file2(self, mock_log):

        """Function:  test_create_new_file2

        Description:  Test with no existing processed file.

        Arguments:

        """

        mock_log.return_value = True

        pulled_search.update_processed(mock_log, self.fname2, self.file_dict)

        self.assertEqual(file_to_list(self.fname2), self.results)

    @mock.patch("pulled_search.gen_class.Logger")
    def test_create_new_file(self, mock_log):

        """Function:  test_create_new_file

        Description:  Test with no existing processed file.

        Arguments:

        """

        mock_log.return_value = True

        pulled_search.update_processed(mock_log, self.fname2, self.file_dict)

        self.assertTrue(os.path.isfile(self.fname2))

    def tearDown(self):

        """Function:  tearDown

        Description:  Clean up of unit testing.

        Arguments:

        """

        if os.path.isfile(self.fname):
            os.remove(self.fname)

        if os.path.isfile(self.fname2):
            os.remove(self.fname2)


if __name__ == "__main__":
    unittest.main()
