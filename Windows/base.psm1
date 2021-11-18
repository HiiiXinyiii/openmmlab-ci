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
    $torchVersion = ""
    if ('1.5.0' -eq $torch) {
        $torchVersion = "0.6.0"
    } elseif ('1.6.0' -eq $torch) {
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
        Write-Host "Torch not supported"
        throw;
    }
    return $torchVersion
}

function GetCudaValue() {
    param (
        [string] $cuda
    )
    $cudaValue = ""
    if ('cuda92' -eq $cuda) {
        $cudaValue = "9.2"
    } elseif ('cuda100' -eq $cuda) {
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
    } elseif ('nocuda' -eq $cuda) {
        $cudaValue = ""
    } else {
        Write-Host "Cuda not supported."
        throw;
    }
    return $cudaValue
}

function GetCudaArchList() {
    param (
        [string] $cuda
    )
    $cudaArchList = ""
    if ('cuda92' -eq $cuda) {
        $cudaArchList = "6.0;7.0"
    } elseif ('cuda110' -eq $cuda) {
        $cudaArchList = "3.5;3.7;5.0;5.2;5.3;6.0;6.2;6.2;7.0;7.2;7.5;8.0"
    } elseif ('cuda111' -eq $cuda) {
        $cudaArchList = "3.5;3.7;5.0;5.2;5.3;6.0;6.2;6.2;7.0;7.2;7.5;8.0;8.6"
    } elseif ('cuda113' -eq $cuda) {
        $cudaArchList = "3.5;3.7;5.0;5.2;5.3;6.0;6.2;6.2;7.0;7.2;7.5;8.0;8.6"
    } elseif ('nocuda' -eq $cuda) {
        $cudaArchList = ""
    } else {
        $cudaArchList = "3.5;3.7;5.0;5.2;5.3;6.0;6.2;6.2;7.0;7.2;7.5"
    }
    return $cudaArchList
}

function GetPythonValue() {
    # Params: py38
    # Return: python=3.8
    param (
        [string] $python
    )

    # TODO: value changed after returned
    # $tmp = $python
    # If ($tmp -match '^\D*(\d{2}).*$') {
    #     "{0}" -f $Matches[1]
    # }
    # $value = $Matches[1].Insert(1, ".")
    if ("py36" -eq $python) {
        $value = "3.6"
    } elseif ("py37" -eq $python) {
        $value = "3.7"
    } elseif ("py38" -eq $python) {
        $value = "3.8"
    } elseif ("py39" -eq $python) {
        $value = "3.9"
    } else {
        Write-Host "Python not supported."
        throw;
    }
    $pythonValue = "python="+$value
    return $pythonValue
}

function CudaTorchMatchCheck() {
    param (
        [string] $cuda,
        [string] $torch
    )

    $cudaValueTorchTuple = [Tuple]::Create($cudaValue, $torch)
    $matchList = New-Object System.Collections.ArrayList
    $matchList.Add((
        [Tuple]::Create("1.5.0", "9.2"),
        [Tuple]::Create("1.5.0", "10.1"),
        [Tuple]::Create("1.5.0", "10.2"),
        [Tuple]::Create("1.6.0", "9.2"),
        [Tuple]::Create("1.6.0", "10.1"),
        [Tuple]::Create("1.6.0", "10.2"),
        [Tuple]::Create("1.7.0", "9.2"),
        [Tuple]::Create("1.7.0", "10.1"),
        [Tuple]::Create("1.7.0", "10.2"),
        [Tuple]::Create("1.7.0", "11.0"),
        [Tuple]::Create("1.8.0", "10.1"),
        [Tuple]::Create("1.8.0", "10.2"),
        [Tuple]::Create("1.8.0", "11.1"),
        [Tuple]::Create("1.9.0", "10.2"),
        [Tuple]::Create("1.9.0", "11.1"),
        [Tuple]::Create("1.10.0", "10.2"),
        [Tuple]::Create("1.10.0", "11.1"),
        [Tuple]::Create("1.10.0", "11.3")
    ))
    if ($matchList -contains $cudaValueTorchTuple) {
        Write-Host "Cuda:$cudaValue & torch:$torch not matched."
        throw;
    }
}

function InstallTorch() {
    param (
        [string] $cuda,
        [string] $cudaValue,
        [string] $torch,
        [string] $torchVision
    )
    if ("" -eq $cudaValue) {
        conda install -y pytorch==$torch torchvision==$torchVision cpuonly -c pytorch
    } else {
        CudaTorchMatchCheck $cuda, $torch
        # if ("1.8.0" -eq $torch ) {
        #     if ("11.0" -le $cudaValue) {
        #         conda install -y pytorch==$torch torchvision==$torchVision cudatoolkit=$cudaValue -c pytorch -c conda-forge
        #     } else {
        #         conda install -y pytorch==$torch torchvision==$torchVision cudatoolkit=$cudaValue -c pytorch
        #     }
        # } else {
        #     conda install -y pytorch==$torch torchvision==$torchVision cudatoolkit=$cudaValue -c pytorch
        # }
        conda install -y pytorch==$torch torchvision==$torchVision cudatoolkit=$cudaValue -c pytorch
    }
    Write-Host "Installing: conda install -y pytorch==$torch torchvision==$torchVision cudatoolkit=$cudaValue -c pytorch"
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