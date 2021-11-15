param($cuda, $python)

$conda_env = $cuda+"_"+$python
conda activate $conda_env
if ($LASTEXITCODE -ne 0) {
    return $LASTEXITCODE
}
pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    return $LASTEXITCODE
}
$cuda_home = "v10.2"
if ('cuda101' -eq $cuda) {
    $cuda_home = "v10.1"
} elseif ('cuda111' -eq $cuda) {
    $cuda_home = "v11.1"
}
$env:CUDA_HOME = "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\$cuda_home"
$env:MMCV_WITH_OPS = 1
$env:MAX_JOBS = 8
$env:TORCH_CUDA_ARCH_LIST="6.1"
python setup.py build_ext
python setup.py develop
pip list
if ($LASTEXITCODE -ne 0) {
    return $LASTEXITCODE
}