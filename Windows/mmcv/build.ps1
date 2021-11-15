param($cuda, $python, $torch, $mmcv)
Write-Host "$cuda, $python, $torch, $mmcv"
$script = "$PSScriptRoot\..\base\base.ps1"
. "$script"

$baseCondaEnv = SetCondaEnvName $cuda, $python, $torch
$tmpEnv = "mmcv"+$mmcv+"_"+$baseCondaEnv

function CondaInstall() {
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
    SetCudaHome $cuda
    # $env:MMCV_WITH_OPS = 1
    # $env:MAX_JOBS = 8
    # $env:TORCH_CUDA_ARCH_LIST="6.1"
    python setup.py build_ext
    python setup.py develop
    if ($LASTEXITCODE -ne 0) {
        return $LASTEXITCODE
    }
    pip list
}

CondaInstall