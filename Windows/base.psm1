function SetCondaEnvName() {
    param (
        [string] $cuda,
        [string] $python,
        [string] $torch
    )
    Write-Host "$cuda, $python, $torch"
    return $cuda+"_"+$python+"_torch"+$torch
}

function GetTorchVision() {
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
    } elseif ('cuda113' -eq $cuda) {
        $cudaValue = "11.3"
    } else {
        Write-Host "Cuda not supported."
        throw;
    }
    return $cudaValue
}

function GetPythonValue() {
    param (
        [string] $python
    )
    $pythonValue = "python"
    $value = $python - replace "[^0-9]", ''
    $pythonValue = $pythonValue + $value.Insert(1, ".")
    return $pythonValue
}

function InstallTorch () {
    param (
        [string] $cuda,
        [string] $cudaValue,
        [string] $torch,
        [string] $torchVision
    )
    if ("cpu" -ne $cuda) {
        conda install -y pytorch==$torch torchvision==$torchVision cudatoolkit=$cudaValue -c torch
    } else {
        conda install -y pytorch==$torch torchvision==$torchVision cpuonly -c torch
    }
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Torch install failed."
        throw;
    }
}

function SetCudaHome() {
    param (
        [string] $cuda
    )
    $cudaValue = GetCudaValue $cuda
    $cudaHome = "v"+$cudaValue
    $env:CUDA_HOME = "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\$cudaHome"
}