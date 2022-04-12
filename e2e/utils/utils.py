from cmath import log
import os
import logging
import yaml
import cup
import shutil
import requests

#
METAFILE = "model-index.yml"        # In OpenMMLab system, the file name is fixed
CODE_PATH = "/opt/mmpose"
CODEBASE_PATH = "/tmp/"

# About github url
GROUP_NAME = "open-mmlab"
MMCLS_CB = "mmclassification"
MMCLS_URL = f"https://github.com/{GROUP_NAME}/{MMCLS_CB}.git"
MMDET_CB = "mmdetection"
MMDET_URL = f"https://github.com/{GROUP_NAME}/{MMDET_CB}.git"
MMPOSE_CB = "mmpose"
MMPOSE_URL = f"https://github.com/{GROUP_NAME}/{MMPOSE_CB}.git"
MMPOSE_PATH = CODEBASE_PATH + MMPOSE_CB + "/"


def python_exec(cmd, timeout=None):
    logging.getLogger().debug(cmd)
    shellobj = cup.shell.ShellExec()
    ret = shellobj.run("cd %s && python %s" % (CODE_PATH, cmd), timeout)
    logging.getLogger().debug(ret)
    if ret['returncode'] == 0:
        logging.getLogger().debug(ret["stdout"])
        return True, ret["stdout"]
    else:
        logging.warning(ret['stderr'])
        return False, ret['stderr']


def get_gitfile(file_path, repo, branch):
    file_name = file_path.split("/")[-1]
    url = f"https://raw.githubusercontent.com/{GROUP_NAME}/{repo}/{branch}/{file_path}"
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(file_name, "wb") as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
        return file_name
    else:
        logging.getLogger().error("Get file from git url: %s failed." % url)
        return None


# get all metafiles according to remote model-index.yml (from github)
def get_git_metafiles(repo, branch):
    """
    Function: get all metafiles according to remote model-index.yml (from github)
    """
    metafile = get_gitfile(METAFILE, repo, branch)
    with open(metafile, "r") as f:
        meta = yaml.safe_load(f)
    return meta["Import"]


# get all metafiles according to local model-index.yml
def get_metafiles(code_path):
    """
    Function: get the metafile of all configs from model-index.yml
    """
    metafile = os.path.join(code_path, METAFILE)
    with open(metafile, "r") as f:
        meta = yaml.safe_load(f)
    return meta["Import"]


# get the checkpoint file corresponding to the config file
def get_cpt(file_path, code_path):
    """
    Function； get the checkpoint file corresponding to the config file

    :param file_path: the config file directory
    :param code_path: the code root path

    Note: file_path we have to use '/' rather than '\\', we simply compare string with metayaml which uses '/'
    """

    cpt_name = None
    metafiles = get_metafiles(code_path)
    for mf in metafiles:
        # meta_file = get_gitfile(mf, repo, branch)
        meta_file = os.path.join(code_path, mf)
        with open(meta_file, "r") as f:
            meta = yaml.safe_load(f)
        for model in meta["Models"]:
            if "Config" in model and model["Config"] == file_path:
                r = requests.get(model["Weights"])
                cpt_name = model["Weights"].split("/")[-1]
                logging.getLogger().info(cpt_name)
                with open(cpt_name, "wb") as f:
                    f.write(r.content)
                return cpt_name
            else:
                logging.getLogger().warning("%s Config not in model" % file_path)
    return cpt_name
