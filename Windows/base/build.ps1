param($cuda, $python, $torch)
. ".\base.ps1"
Write-Host "$cuda, $python, $torch"
$condaEnv = SetCondaEnvName $cuda, $python, $torch

function CondaInstall() {
    $torchVision = GetTorchVision $torch
    $cudaValue = GetCudaValue $cuda
    $cudaHome = "v"+$cudaValue
    conda create -y -n $condaEnv
    conda activate $condaEnv
    if ($LASTEXITCODE -ne 0) {
        return $LASTEXITCODE
    }
    SetCudaHome $cuda
    $env:MMCV_WITH_OPS = 1
    $env:MAX_JOBS = 8
    $env:TORCH_CUDA_ARCH_LIST="6.1"
    InstallTorch $cuda, $cudaValue, $torchVision
    pip install -r "$PSScriptRoot\requirements.txt"
    conda deactivate
}

CondaInstall
return $LASTEXITCODE