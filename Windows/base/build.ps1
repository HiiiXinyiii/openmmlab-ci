param($cuda, $python, $torch)
$scriptDir = Split-Path -parent $MyInvocation.MyCommand.Path
Write-Host "$scriptDir"
Import-Module $scriptDir\..\base.psm1

Write-Host "$cuda, $python, $torch"
$condaEnv = SetCondaEnvName $cuda $python $torch

function CondaInstall() {
    try {
        $torchVision = GetTorchVision $torch
        $cudaValue = GetCudaValue $cuda
        $cudaArchList = GetCudaArchList $cuda
        SetCudaHome $cuda
        $pythonEnv = GetPythonValue $python
        Write-Host "$python"
        Write-Host "$pythonEnv"
        Write-Host "$cudaArchList"
        Write-Host "torchVision: $torchVision"
        conda env remove -y -n $condaEnv
        conda create -y -n $condaEnv $pythonEnv
        Write-Host "conda activate $condaEnv"
        conda activate $condaEnv
        if ($LASTEXITCODE -ne 0) {
            Write-Host "Conda activate $condaEnv failed."
            return $LASTEXITCODE
        }
        Write-Host "Conda env list"
        conda env list
        $env:MMCV_WITH_OPS = 1
        $env:MAX_JOBS = 8
        $env:TORCH_CUDA_ARCH_LIST=$cudaArchList
        $env:PATH += ";C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Tools\MSVC\14.27.29110\bin\Hostx86\x64"
        InstallTorch $cuda $cudaValue $torch $torchVision
        if ($LASTEXITCODE -ne 0) {
            return $LASTEXITCODE
        }
        pip install -r "$PSScriptRoot\requirements.txt"
        conda deactivate
    }
    catch {
        Write-Host "Conda install failed."
        throw;
    }
}

CondaInstall
return $LASTEXITCODE