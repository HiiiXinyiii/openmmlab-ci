import logging
import yaml
import cup
import shutil
import requests

GROUP_NAME = "open-mmlab"
METAFILE   = "model-index.yml"


def python_exec(cmd, is_print=True, timeout=None):
    return cup.shell.execshell("python %s" % cmd, b_printcmd=is_print, timeout=timeout)


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
        return None


def get_metafiles(repo, branch):
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


def get_cpt(file_path, repo, branch):
    cpt_name = None
    metafiles = get_metafiles(repo, branch)
    for mf in metafiles:
        meta_file = get_gitfile(mf, repo, branch)
        with open(meta_file, "r") as f:
            meta = yaml.safe_load(f)
        for model in meta["Models"]:
            if model["Config"] == file_path:
                r = requests.get(model["Weights"])
                cpt_name = model["Weights"].split("/")[-1]
                logging.error(cpt_name)
                with open(cpt_name, "wb") as f:
                    f.write(r.content)
                return cpt_name
    return cpt_name