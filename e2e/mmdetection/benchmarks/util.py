import logging
import cup
import pytest


def python_exec(cmd, timeout=None):
    logging.getLogger().debug(cmd)
    shellobj = cup.shell.ShellExec()
    ret = shellobj.run("cd %s && python %s" % (pytest.CODEB_PATH, cmd), timeout)
    logging.getLogger().debug(ret)
    if ret['returncode'] == 0:
        logging.getLogger().debug(ret["stdout"])
        return True, ret["stdout"]
    else:
        logging.warning(ret['stderr'])
        return False, ret['stderr']