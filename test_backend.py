from backend.powershell import PowershellBackend
from backend.pwsh import PwshBackend

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
