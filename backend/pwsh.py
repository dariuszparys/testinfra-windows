from testinfra.backend import base
from testinfra.modules.file import File
from modules.windowsfile import WindowsFile

import platform
import base64


old_get_module_class = File.get_module_class


@classmethod
def patched_get_module_class(cls, host):
    if platform.system() == "Windows":
        return WindowsFile
    return old_get_module_class(host)


File.get_module_class = patched_get_module_class


class PwshBackend(base.BaseBackend):
    def __init__(self, *args, **kwargs):
        NAME = "pwsh"
        super().__init__(NAME, **kwargs)

    def get_pytest_id(self):
        return "pwsh"

    @classmethod
    def get_hosts(cls, host, **kwargs):
        return [host]


    def run(self, command: str):
        encoded_bytes = base64.b64encode(command.encode("utf-16-le"))
        encoded_str = str(encoded_bytes, "utf-8")
        command = f"pwsh -EncodedCommand {encoded_str}"
        return self.run_local(command)

    def encode(self, data):
        return data
    
    def decode(self, data):
        return data.decode("utf-8")
