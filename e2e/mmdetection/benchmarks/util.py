import logging
import cup
import pytest


def python_exec(cmd, timeout=None):
    logging.getLogger().info(cmd)
    shellobj = cup.shell.ShellExec()
    ret = shellobj.run(cmd, timeout)
    logging.getLogger().info(ret)
    if ret['returncode'] == 0:
        logging.getLogger().info(ret["stdout"])
        return True, ret["stdout"]
    else:
        logging.warning(ret['stderr'])
        return False, ret['stderr']