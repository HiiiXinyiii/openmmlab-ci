param($cuda, $python, $torch, $mmcv)
Write-Host "$cuda, $python, $torch, $mmcv"
. ".\base\build.ps1"

$baseCondaEnv = SetCondaEnvName $cuda, $python, $torch
$tmpEnv = "mmcv"+$mmcv+"_"+$baseCondaEnv

conda create -y -n $tmpEnv --clone $baseCondaEnv
conda activate $baseCondaEnv
if ($LASTEXITCODE -ne 0) {
    Write-Host "Conda activate failed."
    return $LASTEXITCODE
}
pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "Pip install failed."
    return $LASTEXITCODE
}
$cudaValue = GetCudaValue $cuda
$cudaHome = "v"+$cudaValue
$env:CUDA_HOME = "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\$cuda_home"
# $env:MMCV_WITH_OPS = 1
# $env:MAX_JOBS = 8
# $env:TORCH_CUDA_ARCH_LIST="6.1"
python setup.py build_ext
python setup.py develop
pip list
if ($LASTEXITCODE -ne 0) {
    return $LASTEXITCODE
}