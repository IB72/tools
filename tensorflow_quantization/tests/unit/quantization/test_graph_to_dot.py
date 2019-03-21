import pytest
import sys
from mock import MagicMock, mock_open, patch

from quantization.graph_to_dot import main
from test_utils.io import catch_stdout


@pytest.fixture()
def mock_gfile(patch):
    return patch("gfile")


@pytest.fixture(autouse=True)
def mock_flags(patch):
    return patch("FLAGS")


@pytest.fixture
def mock_graph_pb2(patch):
    return patch("graph_pb2")


@pytest.fixture
def mock_open_fixture(patch):
    return patch("open", mock_open())


def test_main(mock_flags, mock_gfile, mock_graph_pb2, mock_open_fixture):
    """Asserts passing in valid input results in return of 0"""
    mock_gfile.Exists.return_value = True
    mock_flags.input_binary = True
    mock_flags.dot_output = 'dot_file'
    mock_graph_pb2.GraphDef.return_value.node = [MagicMock(input=['a']), MagicMock(input=['^', 'b'])]

    with catch_stdout() as output:
        main(["--flag", "arg"])
        output = output.getvalue()
    assert "Created DOT file 'dot_file'." in output


def test_main_bad_flags(mock_gfile, mock_flags):
    """Asserts passing in bad input causes return of -1"""
    mock_gfile.Exists.return_value = False
    mock_flags.graph = "/notafile"

    with catch_stdout() as output:
        func_return = main(["--flag", "arg"])
        output = output.getvalue()
    assert func_return == -1
    assert output == "Input graph file '/notafile' does not exist!\n"
