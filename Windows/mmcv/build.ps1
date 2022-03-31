param($benv, $mmcv)
Write-Host "$benv, $mmcv"
$scriptDir = Split-Path -parent $MyInvocation.MyCommand.Path
Write-Host "$scriptDir"
Import-Module $scriptDir\..\base.psm1

$baseCondaEnv = $benv
$tmpEnv = "mmcv"+$mmcv+"_"+$baseCondaEnv
$prefixCondaPath = GetCondaEnvPath
$cuda, $python, $torch = ParseCondaEnv $benv
Write-Host "$cuda, $python, $torch"
$cudaArchList = GetCudaArchList $cuda

function CondaInstall() {
    TorchPythonMatchCheck $torch, $python

    conda init powershell
    try {
        Write-Host "pip uninstall -y mmcv-full mmcv"
        pip uninstall -y mmcv-full mmcv
        $tmpEnvPath = Join-Path $prefixCondaPath -ChildPath $tmpEnv
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
    python -c "import torch"
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Torch not installed."
        throw
    }
    # TODO: remove debug
    Write-Host "$env:TORCH_CUDA_ARCH_LIST"
    # TODO: move pip install ninja into requirements.txt
    pip install ninja
    pip install -r requirements/build.txt
    pip install -r requirements/optional.txt
    pip install -r requirements/runtime.txt
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
    python setup.py build_ext
    Write-Host "Start python setup.py build_ext."
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Python setup.py build_ext failed."
        throw
    }
    # python setup.py develop
    Write-Host "Start python setup.py install."
    python setup.py install
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Python setup.py install failed."
        throw
    }
    Write-Host "Python setup.py install successfully."
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
        Write-Host "Verify version failed."
        throw;
    }
    python .dev_scripts/check_installation.py
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Verify failed."
        throw;
    }
}

CondaInstall
Verify $torch $mmcv
return $LASTEXITCODE