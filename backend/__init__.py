from testinfra.backend import BACKENDS

BACKENDS["pwsh"] = "backend.pwsh.PwshBackend"
BACKENDS["powershell"] = "backend.powershell.PowershellBackend"
