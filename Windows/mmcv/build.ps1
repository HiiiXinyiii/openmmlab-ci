param($cuda, $python, $torch, $mmcv)
Write-Host "$cuda, $python, $torch, $mmcv"
$scriptDir = Split-Path -parent $MyInvocation.MyCommand.Path
Write-Host "$scriptDir"
Import-Module $scriptDir\..\base.psm1

$baseCondaEnv = SetCondaEnvName $cuda $python $torch
$tmpEnv = "mmcv"+$mmcv+"_"+$baseCondaEnv
$cudaArchList = GetCudaArchList $cuda
$prefixCondaPath = "C:\Users\user\miniconda3\envs\"

function CondaInstall() {
    TorchPythonMatchCheck $torch, $python

    conda init powershell
    try {
        Write-Host "pip uninstall -y mmcv-full mmcv"
        pip uninstall -y mmcv-full mmcv
        $tmpEnvPath = $prefixCondaPath+$tmpEnv
        if (Test-Path $tmpEnvPath) {
            Write-Host "Start remove item in Path:$tmpEnvPath"
            Remove-Item -Path $tmpEnvPath -Recurse
        }
        conda remove -y --name $tmpEnv --all
        Write-Host "Start conda create -y -n $tmpEnv --clone $baseCondaEnv"
        conda create -y -n $tmpEnv --clone $baseCondaEnv
        if ($LASTEXITCODE -ne 0) {
            Write-Host "Conda create failed."
            throw
        }
    } catch {
        Write-Host "Conda failed."
        throw
    }
    conda activate $tmpEnv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Conda activate failed."
        throw
    }
    Write-Host "Conda env list"
    conda env list
    # TODO: remove debug
    Write-Host "$env:TORCH_CUDA_ARCH_LIST"
    # TODO: move pip install ninja into requirements.txt
    pip install ninja
    pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Pip install requirements.txt failed."
        throw
    }
    SetCudaHome $cuda
    Write-Host "$env:CUDA_HOME"
    $env:MMCV_WITH_OPS = 1
    $env:MAX_JOBS = 8
    $env:TORCH_CUDA_ARCH_LIST=$cudaArchList
    SetMSVCEnvPath $cuda
    Write-Host "$env:PATH"
    # python setup.py build_ext
    # if ($LASTEXITCODE -ne 0) {
    #     Write-Host "Python setup.py build_ext failed."
    #     throw
    # }
    # # python setup.py develop
    # python setup.py install
    # if ($LASTEXITCODE -ne 0) {
    #     Write-Host "Python setup.py install failed."
    #     throw
    # }
    pip list
    python setup.py bdist_wheel
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Python setup.py bdist_wheel failed."
        throw
    }
}

function Verify() {
    param (
        [string] $torch,
        [string] $mmcv
    )

    # $path = (Get-Item .).FullName
    python "$PSScriptRoot\verify.py" --torch-version $torch --mmcv-version $mmcv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Verify failed."
        throw;
    }
}

CondaInstall
Verify $torch $mmcv
return $LASTEXITCODE