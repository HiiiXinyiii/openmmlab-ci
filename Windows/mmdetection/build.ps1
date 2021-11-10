param($cuda, $python, $mmcv)

conda activate $cuda_$python
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
        if ($cur_mmcv -ne $mmcv) {
            Write-Host "$cur_mmcv is not euqal to $mmcv"
        }
        return $cur_mmcv
    }
    catch {
        Write-Host "Get mmcv version failed"
        # TODO: Install mmcv
        throw
    }
}

function InstallPackage() {
    pip install -r .\requirements\/build.txt
    python .\setup.py develop
    pip list
}

Get-MMCV $mmcv
InstallPackage