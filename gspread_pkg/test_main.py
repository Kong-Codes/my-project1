import pytest
from unittest import mock
from main import open_spreadsheet, create_spreadsheet, new_worksheet, select_spreadsheet, spreadsheet_format



# Test cases for open spreadsheet function
def test_open_spreadsheet():
    assert open_spreadsheet("project 1202")
    with pytest.raises(ValueError, match="The sheet name expected a string object"):
        assert open_spreadsheet(1022)
    with pytest.raises(ValueError, match="The sheet name expected a string object"):
        assert open_spreadsheet(True)


# Test cases for create spreadsheet function
def test_create_spreadsheet():
    assert create_spreadsheet("Opening")
    with pytest.raises(ValueError, match="The sheet name expected a string object"):
        assert create_spreadsheet(22.343)


# Test cases for select spreadsheet function
def test_select_spreadsheet():
    assert select_spreadsheet("project 1202", "Sheet1")
    with pytest.raises(ValueError, match="The input expected a string object"):
        assert select_spreadsheet(1202, "Sheet1")


# Test cases for worksheet format
def test_format_spreadsheet():
    assert spreadsheet_format('project 1202', 'Sheet1', 'A1', 'C1')
    with pytest.raises(ValueError, match="The input expected a string object e.g 'A1' for the cols and rows input."
                                        "Wrong input expected a string object."):
        assert spreadsheet_format(110, float, 1, 3)


def test_new_worksheet():
    with pytest.raises(FileExistsError, match="This worksheet already exists"):
        assert new_worksheet("project 1202", "Companies", 100, 3)
    with pytest.raises(ValueError, match="The input expected a number/integer for the "
                                         "rows ands cols input, other inputs are strings"):
        assert new_worksheet("project 1202", True, 100, 3)
