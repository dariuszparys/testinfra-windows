from testinfra.backend import base
from testinfra.modules.file import File
from modules.windowsfile import WindowsFile

import platform


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
        super().__init__(NAME, *args, **kwargs)

    def run(self, command: str):
        command = "pwsh -Command \"& { %s }\"" % command
        return self.run_local(command)

    def encode(self, data):
        return data
    
    def decode(self, data):
        return data.decode("utf-8")
