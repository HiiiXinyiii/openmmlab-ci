param($cuda, $python, $mmcv)
Write-Host "$cuda, $python, $mmcv"

$conda_env = $cuda+"_"+$python
conda activate $conda_env
if ($LASTEXITCODE -ne 0) {
    return $LASTEXITCODE
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
        Write-Host "Get mmcv version failed"
        # TODO: Install mmcv
        throw;
    }
}

function InstallPackage() {
    pip uninstall -y mmdet
    pip install -r .\requirements\/build.txt
    python .\setup.py develop
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Install package failed"
        throw;
    }
    pip list
}

Get-MMCV $mmcv
InstallPackage
return $LASTEXITCODE