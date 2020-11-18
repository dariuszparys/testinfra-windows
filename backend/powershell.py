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
        command = "powershell -Command \"& { %s }\"" % command
        return self.run_local(command)


    def encode(self, data):
        return data

    
    def decode(self, data):
        return data.decode("utf-8")
