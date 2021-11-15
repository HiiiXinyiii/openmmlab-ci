param($cuda, $python, $mmcv, $mmdetection)
Write-Host "$cuda, $python, $mmcv, $mmdetection"

$conda_env = $cuda+"_"+$python
# conda activate $conda_env
$tmp_env = $mmdetection+"_"+$conda_env

conda create -y -n $tmp_env --clone $conda_env
conda activate $tmp_env
if ($LASTEXITCODE -ne 0) {
    return $LASTEXITCODE
}

function tearDownWithFail() {
    conda env remove -y -n $tmp_env
}

function Get-MMCV() {
    param(
        [string] $mmcv
    )
    $cur_mmcv_line = pip list | Select-String -Pattern "mmcv"
    Write-Host $cur_mmcv_line
    try {
        $cur_mmcv = [regex]::split($cur_mmcv_line, ",|\s+")[1]
        Write-Host $cur_mmcv
        if ("v$cur_mmcv" -ne $mmcv) {
            Write-Host "$cur_mmcv is not euqal to $mmcv"
            throw;
        }
        return $cur_mmcv
    }
    catch {
        Write-Host "Get mmcv version failed."
        # TODO: Install mmcv
        throw;
    }
}

function InstallPackage() {
    pip uninstall -y mmdet
    pip install ninja
    pip install -r .\requirements\/build.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Install package failed"
        throw;
    }
    Write-Host "Install build.txt successfully."
    python .\setup.py develop
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Install package failed."
        throw;
    }
    Write-Host "Install package successfully."
    pip list
}

function Verify() {
    # $path = (Get-Item .).FullName
    python "$PSScriptRoot\verify.py"
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Verify failed."
        throw;
    }
}

Get-MMCV $mmcv
InstallPackage
Verify
return $LASTEXITCODE