from backend.powershell import PowershellBackend
from backend.pwsh import PwshBackend
from modules.windowsfile import WindowsFile

import testinfra

def test_powershell_get_version(host):
    command = "(get-host).version.major"

    result = host.run(command)

    assert result.stdout.strip() == "7"
    assert result.rc == 0


def test_powershell_get_output(host):
    command = "(get-host).version.major"

    result = host.check_output(command)

    assert result == "7"


def test_requirements_file_exists(host):
    requirements_file = host.file("requirements.txt")
    assert requirements_file.exists


def test_requirements_file_is_file(host):
    requirements_file = host.file("requirements.txt")
    assert requirements_file.is_file


def test_backend_is_directory(host):
    backend_dir = host.file("backend")
    assert backend_dir.is_directory


def test_123_file_does_not_exists(host):
    non_existent_file = host.file("123.123")
    assert non_existent_file.exists == False




    
