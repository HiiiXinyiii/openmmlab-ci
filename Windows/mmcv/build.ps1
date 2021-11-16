param($cuda, $python, $torch, $mmcv)
Write-Host "$cuda, $python, $torch, $mmcv"
$scriptDir = Split-Path -parent $MyInvocation.MyCommand.Path
Write-Host "$scriptDir"
Import-Module $scriptDir\..\base.psm1

$baseCondaEnv = SetCondaEnvName $cuda $python $torch
$tmpEnv = "mmcv"+$mmcv+"_"+$baseCondaEnv

function CondaInstall() {
    conda env remove -y -n $tmpEnv
    pip uninstall -y mmcv-full mmcv
    conda create -y -n $tmpEnv --clone $baseCondaEnv
    conda activate $tmpEnv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Conda activate failed."
        return $LASTEXITCODE
    }
    pip install ninja
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
return $LASTEXITCODE