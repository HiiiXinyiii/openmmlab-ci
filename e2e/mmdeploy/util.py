import logging
import yaml
import cup
import shutil
import requests

GROUP_NAME = "open-mmlab"
METAFILE   = "model-index.yml"
CODE_PATH  = "/opt/mmdeploy"
CODEBASE_PATH = "/tmp/"
MMDET_CB   = "mmdetection"
MMCLS_CB   = "mmclassification"
MMDET_URL  = "https://github.com/%s/%s.git" % (GROUP_NAME, MMDET_CB)
MMCLS_URL  = "https://github.com/%s/%s.git" % (GROUP_NAME, MMCLS_CB)


def python_exec(cmd, timeout=None):
    logging.getLogger().debug(cmd)
    shellobj = cup.shell.ShellExec()
    ret = shellobj.run("cd %s && python %s" % (CODE_PATH, cmd), timeout)
    logging.getLogger().debug(ret)
    if ret['returncode'] == 0:
        return True, ret["stdout"]
    else:
        logging.warning(ret['stderr'])
        return False, ret['stderr']


def get_gitfile(file_path, repo, branch):
    file_name = file_path.split("/")[-1]
    url = "https://raw.githubusercontent.com/%s/%s/%s/%s" % (GROUP_NAME, repo, branch, file_path)
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(file_name, "wb") as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
        return file_name
    else:
        logging.getLogger().error("Get file from git url: %s failed." % url)
        return None


def get_git_metafiles(repo, branch):
    """
    :param repo:
    :param branch:
    :return:
        return 
    """
    metafile = get_gitfile(METAFILE, repo, branch)
    with open(metafile, "r") as f:
        meta = yaml.safe_load(f)
    return meta["Import"]


def get_metafiles(code_path, branch):
    metafile = code_path+"/"+METAFILE
    with open(metafile, "r") as f:
        meta = yaml.safe_load(f)
    return meta["Import"]


def get_cpt(file_path, code_path, branch):
    cpt_name = None
    metafiles = get_metafiles(code_path, branch)
    for mf in metafiles:
        # meta_file = get_gitfile(mf, repo, branch)
        meta_file = code_path+mf
        with open(meta_file, "r") as f:
            meta = yaml.safe_load(f)
        for model in meta["Models"]:
            if "Config" in model and model["Config"] == file_path:
                r = requests.get(model["Weights"])
                cpt_name = model["Weights"].split("/")[-1]
                logging.getLogger().debug(cpt_name)
                with open(cpt_name, "wb") as f:
                    f.write(r.content)
                return cpt_name
    return cpt_name