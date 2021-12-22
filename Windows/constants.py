from os import path

JENKINS_URL         = "http://ci.openmmlab.sensetime.com:8080"
USER_NAME           = "admin"
USER_TOKEN          = "117e4c4117f7497b0452d690b135c62ddf"

WINDOWS_STORAGE_DIR = "C:\\Workspace\\bdist"
LINUX_STORAGE_DIR   = path.join(path.expanduser("~"), "Workspace/bdist")

DEBUG_BASE_ENVS     = [
    # 'cuda113_py36_torch1.10.0',
    # 'cuda111_py36_torch1.8.0',
    # 'cuda111_py37_torch1.8.0',
    # 'cuda111_py38_torch1.8.0',
    # 'cuda111_py39_torch1.8.0',
    # 'cuda111_py36_torch1.9.0',
    # 'cuda111_py37_torch1.9.0',
    # 'cuda111_py38_torch1.9.0',
    # 'cuda111_py39_torch1.9.0',
    'cuda111_py37_torch1.10.0',
    'cuda111_py38_torch1.10.0',
    'cuda111_py39_torch1.10.0',
    # 'cuda113_py36_torch1.10.0',
    # 'cuda113_py37_torch1.10.0',
    # 'cuda113_py38_torch1.10.0',
    # 'cuda113_py39_torch1.10.0',
]
DEFAULT_BASE_ENVS   = [
    'cuda92_py36_torch1.5.0',
    'cuda92_py37_torch1.5.0',
    'cuda92_py38_torch1.5.0',
    'cuda101_py36_torch1.5.0',
    'cuda101_py37_torch1.5.0',
    'cuda101_py38_torch1.5.0',
    'cuda102_py36_torch1.5.0',
    'cuda102_py37_torch1.5.0',
    'cuda102_py38_torch1.5.0',
    'cuda92_py36_torch1.6.0',
    'cuda92_py37_torch1.6.0',
    'cuda92_py38_torch1.6.0',
    'cuda101_py36_torch1.6.0',
    'cuda101_py37_torch1.6.0',
    'cuda101_py38_torch1.6.0',
    'cuda102_py36_torch1.6.0',
    'cuda102_py37_torch1.6.0',
    'cuda102_py38_torch1.6.0',
    'cuda92_py36_torch1.7.0',
    'cuda92_py37_torch1.7.0',
    'cuda92_py38_torch1.7.0',
    'cuda101_py36_torch1.7.0',
    'cuda101_py37_torch1.7.0',
    'cuda101_py38_torch1.7.0',
    'cuda102_py36_torch1.7.0',
    'cuda102_py37_torch1.7.0',
    'cuda102_py38_torch1.7.0',
    'cuda110_py36_torch1.7.0',
    'cuda110_py37_torch1.7.0',
    'cuda110_py38_torch1.7.0',
    'cuda101_py36_torch1.8.0',
    'cuda101_py37_torch1.8.0',
    'cuda101_py38_torch1.8.0',
    'cuda101_py39_torch1.8.0',
    'cuda102_py36_torch1.8.0',
    'cuda102_py37_torch1.8.0',
    'cuda102_py38_torch1.8.0',
    'cuda102_py39_torch1.8.0',
    'cuda111_py36_torch1.8.0',
    'cuda111_py37_torch1.8.0',
    'cuda111_py38_torch1.8.0',
    'cuda111_py39_torch1.8.0',
    'cuda102_py36_torch1.9.0',
    'cuda102_py37_torch1.9.0',
    'cuda102_py38_torch1.9.0',
    'cuda102_py39_torch1.9.0',
    'cuda111_py36_torch1.9.0',
    'cuda111_py37_torch1.9.0',
    'cuda111_py38_torch1.9.0',
    'cuda111_py39_torch1.9.0',
    'cuda102_py36_torch1.10.0',
    'cuda102_py37_torch1.10.0',
    'cuda102_py38_torch1.10.0',
    'cuda102_py39_torch1.10.0',
    'cuda111_py36_torch1.10.0',
    'cuda111_py37_torch1.10.0',
    'cuda111_py38_torch1.10.0',
    'cuda111_py39_torch1.10.0',
    'cuda113_py36_torch1.10.0',
    'cuda113_py37_torch1.10.0',
    'cuda113_py38_torch1.10.0',
    'cuda113_py39_torch1.10.0',
    'nocuda_py36_torch1.5.0',
    'nocuda_py37_torch1.5.0',
    'nocuda_py38_torch1.5.0',
    'nocuda_py36_torch1.6.0',
    'nocuda_py37_torch1.6.0',
    'nocuda_py38_torch1.6.0',
    'nocuda_py36_torch1.7.0',
    'nocuda_py37_torch1.7.0',
    'nocuda_py38_torch1.7.0',
    'nocuda_py36_torch1.8.0',
    'nocuda_py37_torch1.8.0',
    'nocuda_py38_torch1.8.0',
    'nocuda_py39_torch1.8.0',
    'nocuda_py36_torch1.9.0',
    'nocuda_py37_torch1.9.0',
    'nocuda_py38_torch1.9.0',
    'nocuda_py39_torch1.9.0',
    'nocuda_py36_torch1.10.0',
    'nocuda_py37_torch1.10.0',
    'nocuda_py38_torch1.10.0',
    'nocuda_py39_torch1.10.0'
]