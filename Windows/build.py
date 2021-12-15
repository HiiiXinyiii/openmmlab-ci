import os
import sys
import argparse
import platform
from time import sleep
import traceback
from api4jenkins import Jenkins
import constants

WINDOWS_JOB_NAME = "build-on-windows-commit"
# WINDOWS_JOB_NAME = "debug"
OS_NAME = platform.system()

def parse_base_env(base_env):
    tmp = base_env.split("_")
    cuda = tmp[0]
    py = tmp[1]
    torch = tmp[2]
    return (cuda, py, torch)


def get_storage_root_dir():
    root_dir = None
    if OS_NAME == "Windows":
        root_dir = constants.WINDOWS_STORAGE_DIR
    elif OS_NAME == "Linux":
        root_dir = constants.LINUX_STORAGE_DIR
    else:
        raise Exception("Not supported os")
    return root_dir


def get_storage_dir(base_env, repo_name, repo_version):
    cuda, py, torch = parse_base_env(base_env)
    root_dir = get_storage_root_dir()
    if not os.path.exists(root_dir):
        os.makedirs(root_dir)
    if OS_NAME == "Windows":
        file_path = os.path.join(root_dir, "%s//%s//%s//%s" % (repo_name, repo_version, cuda, torch))
    elif OS_NAME == "Linux":
        file_path = os.path.join(root_dir, "%s/%s/%s/%s" % (repo_name, repo_version, cuda, torch))
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    return file_path


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    arg_parser.add_argument(
        "--repo",
        default="mmcv",
        help="repo name")
    arg_parser.add_argument(
        "--version",
        default="repo version",
        help="repo version")
    arg_parser.add_argument(
        "--commit",
        default="repo commit",
        help="repo commit")
    
    args = arg_parser.parse_args()

    repo_name = args.repo
    repo_version = args.version
    repo_commit = args.commit
    if not repo_name or not repo_version or not repo_commit:
        print("Input repo params invalid")
        sys.exit(-2)

    jclient = Jenkins(constants.JENKINS_URL, auth=(constants.USER_NAME, constants.USER_TOKEN), max_retries=3)
    job_name = '%s/%s' % (repo_name, WINDOWS_JOB_NAME)
    building_list = []
    if repo_name == "mmcv":
        job = jclient.get_job(job_name)
        for base_env in constants.DEBUG_BASE_ENVS:
            print(base_env)
            # build = job.get_pending_input().submit(REPO_TAG=repo_version, COMMIT_ID=repo_commit, BASE_ENV=base_env)
            item = jclient.build_job(job_name, REPO_TAG=repo_version, COMMIT_ID=repo_commit, BASE_ENV=base_env)
            build = None
            while build is None:
                build = item.get_build()
                sleep(2)
            print(build)
            description = "%s%s_%s" % (repo_name, repo_version, base_env)
            build.set_description(description)
            building_list.append(build)
            print(base_env, build.id)
    elif repo_name == "mmdetection":
        pass
    
    while building_list:
        for build in building_list:
            if not build.building:
                # Remove from `build_list`
                building_list.remove(build)
                print(build.id, build.result)
                # Get artifacts
                if build.result == "SUCCESS":
                    for artifacts in build.get_artifacts():
                        file_path = get_storage_dir(base_env, repo_name, repo_version)
                        file_name = os.path.join(file_path, artifacts.name)
                        print(build.id, file_name)
                        if os.path.exists(file_name):
                            os.remove(file_name)
                        artifacts.save(file_name)
            else:
                continue