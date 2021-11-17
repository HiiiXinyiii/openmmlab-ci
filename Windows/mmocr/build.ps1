param($cuda, $python, $torch, $mmcv, $mmdetection, $mmocr)
$scriptDir = Split-Path -parent $MyInvocation.MyCommand.Path
Write-Host "$scriptDir"
Import-Module $scriptDir\..\base.psm1

Write-Host "$cuda, $python, $torch, $mmcv, $mmdetection"
$baseCondaEnv = SetCondaEnvName $cuda $python $torch
$mmdetEnv = "mmdet"+$mmdetection+"_"+"mmcv"+$mmcv+"_"+$baseCondaEnv
$tmpEnv = "mmocr"+$mmocr+"_"+$mmdetEnv

function Get-MMCV() {
    param(
        [string] $mmcv
    )
    $curMmcvLine = pip list | Select-String -Pattern "mmcv"
    Write-Host $curMmcvLine
    try {
        $curMmcv = [regex]::split($curMmcvLine, ",|\s+")[1]
        Write-Host $curMmcv
        if ("v$curMmcv" -ne $mmcv) {
            Write-Host "$curMmcv is not euqal to $mmcv"
            throw;
        }
        return $curMmcv
    }
    catch {
        Write-Host "Get mmcv version failed."
        # TODO: Install mmcv
        throw;
    }
}

function InstallPackage() {
    pip uninstall -y mmocr
    pip install -r .\requirements\/build.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Install package failed"
        throw;
    }
    Write-Host "Install build.txt successfully."
    # python setup.py develop
    python setup.py install
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Python setup.py install failed."
        return $LASTEXITCODE
    }
    Write-Host "Install package successfully."
    pip list
    python setup.py bdist_wheel
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Python setup.py bdist_wheel failed."
        return $LASTEXITCODE
    }
}

# function Verify() {
#     # $path = (Get-Item .).FullName
#     python "$PSScriptRoot\verify.py"
#     if ($LASTEXITCODE -ne 0) {
#         Write-Host "Verify failed."
#         throw;
#     }
# }

conda env remove -y -n $tmpEnv
conda create -y -n $tmpEnv --clone $mmdetEnv
conda activate $tmpEnv
if ($LASTEXITCODE -ne 0) {
    return $LASTEXITCODE
}
Get-MMCV $mmcv
InstallPackage
# Verify
return $LASTEXITCODE