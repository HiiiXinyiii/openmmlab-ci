param($cuda, $python, $torch)
$scriptDir = Split-Path -parent $MyInvocation.MyCommand.-Path
Write-Host "$scriptDir"
Import-Module $scriptDir\..\base.psm1

Write-Host "$cuda, $python, $torch"
$condaEnv = SetCondaEnvName $cuda, $python, $torch

function CondaInstall() {
    try {
        $torchVision = GetTorchVision $torch
        $cudaValue = GetCudaValue $cuda
        SetCudaHome $cuda
        conda create -y -n $condaEnv
        conda activate $condaEnv
        if ($LASTEXITCODE -ne 0) {
            return $LASTEXITCODE
        }
    }
    catch {
        Write-Host "Conda install failed."
        throw;
    }
    $env:MMCV_WITH_OPS = 1
    $env:MAX_JOBS = 8
    $env:TORCH_CUDA_ARCH_LIST="6.1"
    InstallTorch $cuda, $cudaValue, $torchVision
    if ($LASTEXITCODE -ne 0) {
        return $LASTEXITCODE
    }
    pip install -r "$PSScriptRoot\requirements.txt"
    conda deactivate
}

CondaInstall
return $LASTEXITCODE