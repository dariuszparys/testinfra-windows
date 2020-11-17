from backend.powershell import PowershellBackend
from backend.pwsh import PwshBackend

import testinfra

command = "(get-host).version.major"

powershell = PowershellBackend("powershell")
result = powershell.run(command)
print(result.stdout)

pwsh = PwshBackend("pwsh")
result = pwsh.run(command)
print(result.stdout)

host = testinfra.get_host("powershell://")
result = host.run(command)
print(result.stdout)