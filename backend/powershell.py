from testinfra.backend import base

class PowershellBackend(base.BaseBackend):
    def __init__(self, *args, **kwargs):
        NAME = "powershell"
        super().__init__("powershell", **kwargs)

    def get_pytest_id(self):
        return "powershell"

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
