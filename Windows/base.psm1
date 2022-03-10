function SetCondaEnvName() {
    param (
        [string] $cuda,
        [string] $python,
        [string] $torch
    )
    Write-Host "$cuda, $python, $torch"
    return $cuda+"_"+$python+"_torch"+$torch
}

function ParseCondaEnv() {
    param (
        [string] $benv
    )

    $env = $benv.Split("_")
    if (3 -ne $env.Length) {
        Write-Host "Invalid env format."
        throw
    }
    $env[2] = $env[2].Split("torch")[-1]
    return $env
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
        $torchVersion = "0.11.0"
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
    # TODO: remove lt 6.0: 3.5;3.7;5.0;5.2;5.3;
    if ('cuda92' -eq $cuda) {
        $cudaArchList = "5.0;5.2;5.3;6.0;7.0"
    } elseif ('cuda110' -eq $cuda) {
        $cudaArchList = "5.0;5.2;5.3;6.0;6.2;6.2;7.0;7.2;7.5;8.0"
    } elseif ('cuda111' -eq $cuda) {
        $cudaArchList = "5.0;5.2;5.3;6.0;6.2;6.2;7.0;7.2;7.5;8.0;8.6"
    } elseif ('cuda113' -eq $cuda) {
        $cudaArchList = "5.0;5.2;5.3;6.0;6.2;6.2;7.0;7.2;7.5;8.0;8.6"
    } elseif ('nocuda' -eq $cuda) {
        $cudaArchList = ""
    } else {
        $cudaArchList = "5.0;5.2;5.3;6.0;6.2;6.2;7.0;7.2;7.5"
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
        [string] $cudaValue,
        [string] $torch
    )
    $cudaValueTorchTuple = [Tuple]::Create($torch, $cudaValue)
    $matchList = New-Object System.Collections.ArrayList
    # TODO: improve
    # $matchList.Add([Tuple]::Create("1.5.0", "9.2"))
    $matchList.Add([Tuple]::Create("1.5.0", "10.1"))
    $matchList.Add([Tuple]::Create("1.5.0", "10.2"))
    # $matchList.Add([Tuple]::Create("1.6.0", "9.2"))
    $matchList.Add([Tuple]::Create("1.6.0", "10.1"))
    $matchList.Add([Tuple]::Create("1.6.0", "10.2"))
    # $matchList.Add([Tuple]::Create("1.7.0", "9.2"))
    $matchList.Add([Tuple]::Create("1.7.0", "10.1"))
    $matchList.Add([Tuple]::Create("1.7.0", "10.2"))
    $matchList.Add([Tuple]::Create("1.7.0", "11.0"))
    $matchList.Add([Tuple]::Create("1.8.0", "10.1"))
    $matchList.Add([Tuple]::Create("1.8.0", "10.2"))
    $matchList.Add([Tuple]::Create("1.8.0", "11.1"))
    $matchList.Add([Tuple]::Create("1.9.0", "10.2"))
    $matchList.Add([Tuple]::Create("1.9.0", "11.1"))
    $matchList.Add([Tuple]::Create("1.10.0", "10.2"))
    $matchList.Add([Tuple]::Create("1.10.0", "11.1"))
    $matchList.Add([Tuple]::Create("1.10.0", "11.3"))
    if (-Not $matchList.Contains($cudaValueTorchTuple)) {
        Write-Host "torch:$torch, cuda:$cudaValue not matched."
        throw;
    }
}

function TorchPythonMatchCheck() {
    param (
        [string] $torch,
        [string] $python
    )

    $torchPythonTuple = [Tuple]::Create($torch, $python)
    $notMatchList = New-Object System.Collections.ArrayList
    $notMatchList.Add([Tuple]::Create("1.5.0", "py39"))
    $notMatchList.Add([Tuple]::Create("1.6.0", "py39"))
    $notMatchList.Add([Tuple]::Create("1.7.0", "py39"))
    if ($notMatchList.Contains($torchPythonTuple)) {
        Write-Host "torch:$torch, python:$python not matched."
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
        Write-Host "Installing: conda install -y pytorch==$torch torchvision==$torchVision cpuonly -c pytorch"
        conda install -y pytorch==$torch torchvision==$torchVision cpuonly -c pytorch -c conda-forge
    } elseif (("11.1" -eq $cudaValue) -and ("1.10.0" -eq $torch)) {
        Write-Host "Skip installing torch1.10.0+cu111"
        # pip install torch==1.10.0+cu111 torchvision==0.11.1+cu111 -f https://download.pytorch.org/whl/torch_stable.html
    } else {
        CudaTorchMatchCheck $cudaValue $torch
        # if ("1.8.0" -le $torch) {
        #     if ("11.0" -le $cudaValue) {
        #         conda install -y pytorch==$torch torchvision==$torchVision cudatoolkit=$cudaValue -c pytorch -c conda-forge
        #     } else {
        #         conda install -y pytorch==$torch torchvision==$torchVision cudatoolkit=$cudaValue -c pytorch
        #     }
        # } else {
        #     conda install -y pytorch==$torch torchvision==$torchVision cudatoolkit=$cudaValue -c pytorch
        # }
        if ("11.0" -le $cudaValue) {
            conda install -y pytorch==$torch torchvision==$torchVision cudatoolkit=$cudaValue -c pytorch -c conda-forge
            Write-Host "Installing: conda install -y pytorch==$torch torchvision==$torchVision cudatoolkit=$cudaValue -c pytorch -c conda-forge"
        } else {
            conda install -y pytorch==$torch torchvision==$torchVision cudatoolkit=$cudaValue -c pytorch
            Write-Host "Installing: conda install -y pytorch==$torch torchvision==$torchVision cudatoolkit=$cudaValue -c pytorch"
        }
        # Write-Host "Installing: conda install -y pytorch==$torch torchvision==$torchVision cudatoolkit=$cudaValue -c pytorch"
        # conda install -y pytorch==$torch torchvision==$torchVision cudatoolkit=$cudaValue -c pytorch
    }
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Torch install failed."
        throw;
    }
}

function UpdateTorchFiles() {
    param (
        [string] $torch,
        [string] $envName
    )

    if ("1.7.0" -ge $torch) {
        $condaEnvPath = GetCondaEnvPath
        $filePath = Join-Path $condaEnvPath -ChildPath "$envName\Lib\site-packages\torch\include"
        Write-Host "Start update torch files."
        # module.h
        $MODULE_FILE_PATH = Join-Path $filePath -ChildPath "\torch\csrc\jit\api\module.h"
        if (Test-Path $MODULE_FILE_PATH) {
            $content = Get-Content $MODULE_FILE_PATH
            $content.replace('constexpr', 'const') | Set-Content $MODULE_FILE_PATH
            $content.replace('CONSTEXPR_EXCEPT_WIN_CUDA', 'const') | Set-Content $MODULE_FILE_PATH
        }
        # cast.h
        $MODULE_FILE_PATH = Join-Path $filePath -ChildPath "\pybind11\cast.h"
        if (Test-Path $MODULE_FILE_PATH) {
            $content = Get-Content $MODULE_FILE_PATH
            $content.replace('return *(this->value)', 'return *((type*)this->value)') | Set-Content $MODULE_FILE_PATH
        }
        # ir.h
        $MODULE_FILE_PATH = Join-Path $filePath -ChildPath "\torch\csrc\jit\ir\ir.h"
        if (Test-Path $MODULE_FILE_PATH) {
            $content = Get-Content $MODULE_FILE_PATH
            $content.replace('static constexpr Symbol Kind', '// static constexpr Symbol Kind') | Set-Content $MODULE_FILE_PATH
        }
    }
}

function GetCondaEnvPath() {
    $CONDA_PATH = Get-Item (Get-Command conda.exe).Path
    $CONDA_ENV_PATH = Join-Path $CONDA_PATH.Directory.Parent.FullName -ChildPath "envs"
    return $CONDA_ENV_PATH
}

function SetCudaHome() {
    param (
        [string] $cuda
    )
    $cudaValue = GetCudaValue $cuda
    $cudaHome = "v"+$cudaValue
    $nvccPath = Get-Item (Get-Command nvcc.exe).Path
    Split-Path $nvccPath -Parent
    $prePath = (Get-Item $nvccPath).Directory.parent.parent.FullName
    Write-Host "CUDA_PATH: $prePath"
    $env:CUDA_HOME = Join-Path $prePath -ChildPath "$cudaHome"
}

function SetMSVCEnvPath() {
    param (
        [string] $cuda
    )

    # if ('cuda92' -eq $cuda) {
    #     # $env:PATH += ";C:\Program Files (x86)\Microsoft Visual Studio\2017\Community\VC\Tools\MSVC\14.16.27023\bin\Hostx86\x64"
    #     $env:PATH += ";C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\bin"
    # } else {
    #     $env:PATH += ";C:\Program Files (x86)\Microsoft Visual Studio\2019\BuildTools\VC\Tools\MSVC\14.29.30133\bin\Hostx86\x64"
    # }
    $env:PATH += ";C:\Program Files (x86)\Microsoft Visual Studio\2019\BuildTools\VC\Tools\MSVC\14.27.29110\bin\Hostx86\x64"
}

# function Get-Hash() {
#     param(
#         [string] $s
#     )
    
#     $md5 = new-object -TypeName System.Security.Cryptography.MD5CryptoServiceProvider
#     $utf8 = new-object -TypeName System.Text.UTF8Encoding
#     $hash = [System.BitConverter]::ToString($md5.ComputeHash($utf8.GetBytes($s)))
#     return $hash
# }