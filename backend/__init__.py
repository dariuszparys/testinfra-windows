from testinfra.backend import base, BACKENDS

import testinfra
import importlib
import os
import urllib.parse

BACKENDS["pwsh"] = "backend.pwsh.PwshBackend"
BACKENDS["powershell"] = "backend.powershell.PowershellBackend"


def _patched_get_backend_class(connection):
    try:
        classpath = BACKENDS[connection]
    except KeyError:
        raise RuntimeError("Unknown connection type '%s'" % (connection,))
    module, name = classpath.rsplit('.', 1)
    return getattr(importlib.import_module(module), name)


def _patched_get_backend(hostspec, **kwargs):
    host, kw = testinfra.backend.parse_hostspec(hostspec)
    for k, v in kwargs.items():
        kw.setdefault(k, v)
    kw.setdefault("connection", "paramiko")
    klass = testinfra.backend.get_backend_class(kw["connection"])
    if kw["connection"] == "local":
        return klass(**kw)
    if kw["connection"] == "powershell":
        return klass(**kw)
    if kw["connection"] == "pwsh":
        return klass(**kw)
    return klass(host, **kw)


testinfra.backend.get_backend = _patched_get_backend
testinfra.backend.get_backend_class = _patched_get_backend_class
