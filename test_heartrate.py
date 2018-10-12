from heartrate import read_my_file
import pytest


@pytest.mark.parametrize("candidate,expected", [
    ('Test.csv', ([0, 1.2, 2.4], [-.375, -.475, 4])),

])
def test_read_my_file(candidate, expected):
    response = read_my_file(candidate)
    assert response[0] == expected[0]
    assert response[1] == expected[1]

