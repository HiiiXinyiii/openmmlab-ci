param($cuda, $python, $torch)

$conda_env = $cuda+"_"+$python+"_"+$torch
Write-Host "$cuda, $python, $torch"

function GetTorchVersion() {
    param (
        [string] $torch
    )
    $torchVersion = "0.7.0"
    if ('1.6.0' -eq $torch) {
        $torchVersion = "0.7.0"
    } elseif ('1.7.0' -eq $torch) {
        $torchVersion = "0.8.0"
    } elseif ('1.7.1' -eq $torch) {
        $torchVersion = "0.8.2"
    } elseif ('1.8.0' -eq $torch) {
        $torchVersion = "0.9.0"
    } elseif ('1.9.0' -eq $torch) {
        $torchVersion = "0.10.0"
    } elseif ('1.10.0' -eq $torch) {
        $torchVersion = "0.11.1"
    } else {
        Write-Host "Not supported"
        throw;
    }
    return $torchVersion
}

function GetCudaValue() {
    param (
        [string] $cuda
    )
    $cudaValue = ""
    if ('cuda100' -eq $cuda) {
        $cudaValue = "10.0"
    } elseif ('cuda101' -eq $cuda) {
        $cudaValue = "10.1"
    } elseif ('cuda102' -eq $cuda) {
        $cudaValue = "10.2"
    } elseif ('cuda110' -eq $cuda) {
        $cudaValue = "11.0"
    } elseif ('cuda111' -eq $cuda) {
        $cudaValue = "11.1"
    } else {
        Write-Host "Cuda not supported."
        throw;
    }
    return $cudaValue
}

function Installtorch () {
    param (
        [string] $cudaValue
    )
    if ("cpu" -ne $cudaValue) {
        conda install -y torch==$torch torchvision=$torchVersion cudatoolkit=$cudaValue -c torch
    } else {
        conda install -y torch==$torch torchvision=$torchVersion cpuonly -c torch
    }
    if ($LASTEXITCODE -ne 0) {
        Write-Host "torch install failed."
        throw;
    }
}

function CondaInstall() {
    $cudaValue = GetCudaValue $cuda
    $cuda_home = "v"+$cudaValue
    conda create -y -n $conda_env
    conda activate $conda_env
    if ($LASTEXITCODE -ne 0) {
        return $LASTEXITCODE
    }
    $torchVersion = GetTorchVersion $cudaValue
    $env:CUDA_HOME = "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\$cuda_home"
    $env:MMCV_WITH_OPS = 1
    $env:MAX_JOBS = 8
    $env:TORCH_CUDA_ARCH_LIST="6.1"

    pip install -y "$PSScriptRoot\requirements.txt"
    conda deactivate $conda_env
}

CondaInstall
return $LASTEXITCODE