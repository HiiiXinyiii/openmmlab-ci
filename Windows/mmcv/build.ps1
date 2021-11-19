param($cuda, $python, $torch, $mmcv)
Write-Host "$cuda, $python, $torch, $mmcv"
$scriptDir = Split-Path -parent $MyInvocation.MyCommand.Path
Write-Host "$scriptDir"
Import-Module $scriptDir\..\base.psm1

$baseCondaEnv = SetCondaEnvName $cuda $python $torch
$tmpEnv = "mmcv"+$mmcv+"_"+$baseCondaEnv
$cudaArchList = GetCudaArchList $cuda

function CondaInstall() {
    TorchPythonMatchCheck $torch, $python

    conda init powershell
    conda remove -y --name $tmpEnv --all
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Conda remove -y --name $tmpEnv --all failed."
        throw
    }
    pip uninstall -y mmcv-full mmcv
    conda create -y -n $tmpEnv --clone $baseCondaEnv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Conda create $tmpEnv from $baseCondaEnv failed."
        throw
    }
    conda activate $tmpEnv
    Write-Host "Conda env list"
    conda env list
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Conda activate failed."
        throw
    }
    Write-Host "$env:PATH"
    # TODO: move pip install ninja into requirements.txt
    pip install ninja
    pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Pip install requirements.txt failed."
        throw
    }
    SetCudaHome $cuda
    $env:MMCV_WITH_OPS = 1
    $env:MAX_JOBS = 8
    $env:TORCH_CUDA_ARCH_LIST=$cudaArchList
    $env:PATH += ";C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Tools\MSVC\14.27.29110\bin\Hostx86\x64"
    python setup.py build_ext
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Python setup.py build_ext failed."
        throw
    }
    # python setup.py develop
    python setup.py install
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Python setup.py install failed."
        throw
    }
    pip list
    python setup.py bdist_wheel
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Python setup.py bdist_wheel failed."
        throw
    }
}

function Verify() {
    # $path = (Get-Item .).FullName
    python "$PSScriptRoot\verify.py"
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Verify failed."
        throw;
    }
}

CondaInstall
Verify
return $LASTEXITCODE