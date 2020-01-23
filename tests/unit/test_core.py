import pytest 
import os

from githubactions.core import command



@pytest.fixture
def env_vars(monkeypatch, request):
    env_vars = { 
        'my var' : '',
        'special char var \r\n];' : '',
        'my var2' : '',
        'my secret' : '',
        'special char secret \r\n;' : '',
        'my secret2' : '',
        'PATH': f"{os.path.sep}".join(['path1', 'path2']),
        'INPUT_MY_INPUT': 'val',
        'INPUT_MISSING': '',
        'INPUT_SPECIAL_CHARS_\'\t"\\': '\'\t"\\ response ',
        'INPUT_MULTIPLE_SPACES_VARIABLE': 'I have multiple spaces'
    }

    for k, v in  env_vars.items():
        monkeypatch.setenv(k, v)

    def fin():
        for k in env_vars:
            monkeypatch.delenv(k)

    request.addfinalizer(fin)


def test_set_env(request, capsys, env_vars):

    command.set_env('my var', 'var val') 
    captured = capsys.readouterr()

    assert captured.out == '::set-env name=my var::var val\n'
    assert os.getenv('my var') == 'var val'

    command.set_env('special char var \r\n];', 'special val')
    captured = capsys.readouterr()

    assert captured.out == '::set-env name=special char var %0D%0A%5D%3B::special val\n'
    assert os.getenv('special char var \r\n];', 'special val')

def test_add_mask(request, capsys):

    command.add_mask('secret val')
    captured = capsys.readouterr()

    assert captured.out == '::add-mask::secret val\n'

def test_add_path(request, capsys, env_vars):

    command.add_path('myPath')
    assert os.getenv('PATH') == f"{os.path.sep}".join(['myPath', 'path1', 'path2'])

def test_get_input(request, capsys, env_vars):
    assert command.get_input('my input') == 'val'

    assert command.get_input('my input', {'required': True}) == 'val'

    assert command.get_input('missing', {'required': False}) == ''

    with pytest.raises(ValueError):
        assert command.get_input('missing', {'required': True})

    assert command.get_input('My InPut') == 'val'

    assert command.get_input('multiple spaces variable') == 'I have multiple spaces'

def test_set_output(request, capsys):

    command.set_output('some output', 'some value')
    captured = capsys.readouterr()

    assert captured.out == '::set-output name=some output::some value\n'

def test_set_failed(capsys) -> None:

    command.set_failed('Failure message')
    captured = capsys.readouterr()

    assert captured.out == '::error::Failure message\n'
