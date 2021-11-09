param($cuda)

conda activate $cuda
pip install -r requirements.txt
$cuda_home = "v10.2"
if('101' -eq $cuda) {
    $cuda_home = "v10.1"
} else if ('111' -eq $cuda) {
    $cuda_home = "v11.1"
}
$env:CUDA_HOME = "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\$cuda_home"
$env:MMCV_WITH_OPS = 1
$env:MAX_JOBS = 8
$env:TORCH_CUDA_ARCH_LIST="6.1"
python setup.py build_ext
python setup.py develop
pip list