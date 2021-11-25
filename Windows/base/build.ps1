param($cuda, $python, $torch)
$scriptDir = Split-Path -parent $MyInvocation.MyCommand.Path
Write-Host "$scriptDir"
Import-Module $scriptDir\..\base.psm1

Write-Host "$cuda, $python, $torch"
$condaEnv = SetCondaEnvName $cuda $python $torch

# $ErrorActionPreference = "Stop"

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
        conda init --all
        if (Test-Path $condaEnv) {
            Write-Host "Start remove item in Path:$condaEnv"
            Remove-Item -Path $condaEnv -Recurse
        }
        conda remove -y --name $condaEnv --all
        if ($LASTEXITCODE -ne 0) {
            Write-Host "Conda remove $condaEnv failed."
            return $LASTEXITCODE
        }
        Write-Host "Conda remove env:$condaEnv successfully."
        Write-Host "Start conda create -y -n $condaEnv $pythonEnv."
        conda create -y -n $condaEnv $pythonEnv
        if ($LASTEXITCODE -ne 0) {
            Write-Host "Conda create $condaEnv failed."
            return $LASTEXITCODE
        }
        UpdateTorchFiles $torch $condaEnv
        Write-Host "conda activate $condaEnv"
        conda activate $condaEnv
        if ($LASTEXITCODE -ne 0) {
            Write-Host "Conda activate $condaEnv failed."
            return $LASTEXITCODE
        }
        Write-Host "Conda env list"
        $env:MMCV_WITH_OPS = 1
        $env:MAX_JOBS = 8
        $env:TORCH_CUDA_ARCH_LIST=$cudaArchList
        # $env:PATH += ";C:\Program Files (x86)\Microsoft Visual Studio\2019\BuildTools\VC\Tools\MSVC\14.29.30133\bin\Hostx86\x64"
        conda env list
        TorchPythonMatchCheck $torch, $python
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