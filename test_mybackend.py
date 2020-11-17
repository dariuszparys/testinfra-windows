from backend.powershell import PowershellBackend
from backend.pwsh import PwshBackend
from modules.windowsfile import WindowsFile

import testinfra

def test_powershell_get_version():
    command = "(get-host).version.major"

    host = testinfra.get_host("powershell://")
    result = host.run(command)

    assert result.stdout.strip() == "5"
    assert result.rc == 0


def test_pwsh_get_version():
    command = "(get-host).version.major"

    host = testinfra.get_host("pwsh://")
    result = host.run(command)

    assert result.stdout.strip() == "7"
    assert result.rc == 0


def test_powershell_get_output():
    command = "(get-host).version.major"

    host = testinfra.get_host("powershell://")
    result = host.check_output(command)

    assert result == "5"


def test_ssh_file_exists():
    host = testinfra.get_host("pwsh://")
    id_rsa_pub = host.file("requirements.txt")
    assert id_rsa_pub.exists


def test_ssh_file_is_file():
    host = testinfra.get_host("pwsh://")
    id_rsa_pub = host.file("requirements.txt")
    assert id_rsa_pub.is_file


def test_ssh_dir_is_directory():
    host = testinfra.get_host("pwsh://")
    id_rsa_pub = host.file("backend")
    assert id_rsa_pub.is_directory


def test_123_file_does_not_exists():
    host = testinfra.get_host("pwsh://")
    id_rsa_pub = host.file("123.123")
    assert id_rsa_pub.exists != "True"




    
