from backend.powershell import PowershellBackend
from backend.pwsh import PwshBackend

import datetime

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


def test_requirements_contains_pylint(host):
    requirements_file = host.file("requirements.txt")
    assert requirements_file.contains("pylint") == True


def test_requirements_file_get_content(host):
    requirements_file = host.file("requirements.txt")
    output = requirements_file.content
    assert len(output) > 0


def test_requirements_file_modified_date(host):
    requirements_file = host.file("requirements.txt")
    mdate = requirements_file.mtime
    assert mdate.year == 2020
