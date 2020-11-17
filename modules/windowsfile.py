import datetime

from testinfra.modules.file import File


class WindowsFile(File):
    def __init__(self, path):
        self.path = path

    @property
    def exists(self):
        command = f"Test-Path -Path \"{self.path}\""
        result = self.check_output(command)
        return result == "True"

    @property
    def is_file(self):
        command = f"Test-Path -Path \"{self.path}\" -PathType leaf"
        result = self.check_output(command)
        return result == "True"

    @property
    def is_directory(self):
        command = f"Test-Path -Path \"{self.path}\" -PathType Container"
        result = self.check_output(command)
        return result == "True"

    @property
    def is_pipe(self):
        raise NotImplementedError

    @property
    def is_socket(self):
        raise NotImplementedError

    @property
    def is_symlink(self):
        raise NotImplementedError

    @property
    def linked_to(self):
        raise NotImplementedError

    @property
    def user(self):
        raise NotImplementedError

    @property
    def uid(self):
        raise NotImplementedError

    @property
    def group(self):
        raise NotImplementedError

    @property
    def gid(self):
        raise NotImplementedError

    @property
    def mode(self):
        raise NotImplementedError

    def contains(self, pattern):
        return self.run_test("grep -qs -- %s %s", pattern, self.path).rc == 0

    @property
    def md5sum(self):
        raise NotImplementedError

    @property
    def sha256sum(self):
        raise NotImplementedError

    def _get_content(self, decode):
        out = self.run_test("cat -- %s", self.path)
        if out.rc != 0:
            raise RuntimeError("Unexpected output %s" % (out,))
        if decode:
            return out.stdout
        return out.stdout_bytes

    @property
    def content(self):
        """Return file content as bytes

        >>> host.file("/tmp/foo").content
        b'caf\\xc3\\xa9'
        """
        return self._get_content(False)

    @property
    def content_string(self):
        """Return file content as string

        >>> host.file("/tmp/foo").content_string
        'café'
        """
        return self._get_content(True)

    @property
    def mtime(self):
        """Return time of last modification as datetime.datetime object

        >>> host.file("/etc/passwd").mtime
        datetime.datetime(2015, 3, 15, 20, 25, 40)
        """
        raise NotImplementedError

    @property
    def size(self):
        """Return size of file in bytes"""
        raise NotImplementedError

    def listdir(self):
        """Return list of items under the directory

        >>> host.file("/tmp").listdir()
        ['foo_file', 'bar_dir']
        """
        out = self.run_test("ls -1 -q -- %s", self.path)
        if out.rc != 0:
            raise RuntimeError("Unexpected output %s" % (out,))
        return out.stdout.splitlines()

    def __repr__(self):
        return "<file %s>" % (self.path,)

    def __eq__(self, other):
        if isinstance(other, File):
            return self.path == other.path
        if isinstance(other, str):
            return self.path == other
        return False

    @classmethod
    def get_module_class(cls, host):
        if host.system_info.type == "linux":
            return GNUFile
        if host.system_info.type == "netbsd":
            return NetBSDFile
        if host.system_info.type.endswith("bsd"):
            return BSDFile
        if host.system_info.type == "darwin":
            return DarwinFile
        if host.system_info.type == "windows":
            return WindowsFile
        raise NotImplementedError


class GNUFile(File):
    @property
    def user(self):
        return self.check_output("stat -c %%U %s", self.path)

    @property
    def uid(self):
        return int(self.check_output("stat -c %%u %s", self.path))

    @property
    def group(self):
        return self.check_output("stat -c %%G %s", self.path)

    @property
    def gid(self):
        return int(self.check_output("stat -c %%g %s", self.path))

    @property
    def mode(self):
        # Supply a base of 8 when parsing an octal integer
        # e.g. int('644', 8) -> 420
        return int(self.check_output("stat -c %%a %s", self.path), 8)

    @property
    def mtime(self):
        ts = self.check_output("stat -c %%Y %s", self.path)
        return datetime.datetime.fromtimestamp(float(ts))

    @property
    def size(self):
        return int(self.check_output("stat -c %%s %s", self.path))

    @property
    def md5sum(self):
        return self.check_output("md5sum %s | cut -d' ' -f1", self.path)

    @property
    def sha256sum(self):
        return self.check_output(
            "sha256sum %s | cut -d ' ' -f 1", self.path)


class BSDFile(File):
    @property
    def user(self):
        return self.check_output("stat -f %%Su %s", self.path)

    @property
    def uid(self):
        return int(self.check_output("stat -f %%u %s", self.path))

    @property
    def group(self):
        return self.check_output("stat -f %%Sg %s", self.path)

    @property
    def gid(self):
        return int(self.check_output("stat -f %%g %s", self.path))

    @property
    def mode(self):
        # Supply a base of 8 when parsing an octal integer
        # e.g. int('644', 8) -> 420
        return int(self.check_output("stat -f %%Lp %s", self.path), 8)

    @property
    def mtime(self):
        ts = self.check_output("stat -f %%m %s", self.path)
        return datetime.datetime.fromtimestamp(float(ts))

    @property
    def size(self):
        return int(self.check_output("stat -f %%z %s", self.path))

    @property
    def md5sum(self):
        return self.check_output("md5 < %s", self.path)

    @property
    def sha256sum(self):
        return self.check_output(
            "sha256 < %s", self.path)


class DarwinFile(BSDFile):

    @property
    def linked_to(self):
        link_script = '''
        TARGET_FILE='{0}'
        cd `dirname $TARGET_FILE`
        TARGET_FILE=`basename $TARGET_FILE`
        while [ -L "$TARGET_FILE" ]
        do
            TARGET_FILE=`readlink $TARGET_FILE`
            cd `dirname $TARGET_FILE`
            TARGET_FILE=`basename $TARGET_FILE`
        done
        PHYS_DIR=`pwd -P`
        RESULT=$PHYS_DIR/$TARGET_FILE
        echo $RESULT
        '''.format(self.path)
        return self.check_output(link_script)


class NetBSDFile(BSDFile):

    @property
    def sha256sum(self):
        return self.check_output(
            "cksum -a sha256 < %s", self.path)
