param($benv, $mmcv, $mmdetection, $mmocr)
$scriptDir = Split-Path -parent $MyInvocation.MyCommand.Path
Write-Host "$scriptDir"
Import-Module $scriptDir\..\base.psm1

Write-Host "$benv, $mmcv, $mmdetection, $mmocr"
$cuda, $python, $torch = ParseCondaEnv $benv
Write-Host "$cuda, $python, $torch"
$prefixCondaPath = GetCondaEnvPath
$mmdetEnv = "mmdet"+$mmdetection+"_"+"mmcv"+$mmcv+"_"+$benv
$tmpEnv = "mmocr"+$mmocr+"_"+$mmdetEnv

function CheckMMCV() {
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
    conda init powershell
    try {
        Write-Host "pip uninstall mmocr"
        pip uninstall -y mmocr
        $tmpEnvPath = Join-Path $prefixCondaPath -ChildPath $tmpEnv
        if (Test-Path $tmpEnvPath) {
            Write-Host "Start remove item in Path:$tmpEnvPath"
            Remove-Item -Path $tmpEnvPath -Recurse
        }
        conda remove -y --name $tmpEnv --all
        Write-Host "Start conda create -y -n $tmpEnv --clone $mmdetEnv"
        conda create -y -n $tmpEnv --clone $mmdetEnv
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
    # Check mmcv version
    CheckMMCV $mmcv

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
    Write-Host "Install setup.py install successfully."
    pip list
    python setup.py bdist_wheel
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Python setup.py bdist_wheel failed."
        return $LASTEXITCODE
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

InstallPackage
if ($LASTEXITCODE -ne 0) {
    Write-Host "Install package failed."
    return $LASTEXITCODE
}
pip install requests
Verify
return $LASTEXITCODE