$jenkinsDir = "C:\Workspace\Jenkins"
$agentFile = "$jenkinsDir\agent.jar"
$jenkinsMasterHost = "http://10.198.21.153:8080"
$curSlaveHost = "10.53.24.125"

function SlaveSetup() {
    if(-not(Test-Path $jenkinsDir)) {
        New-Item -Path $jenkinsDir -ItemType Directory
    }
    Set-Location -Path $jenkinsDir
    if(-not(Test-Path $agentFile)) {
        $client = new-object System.Net.WebClient
        $client.DownloadFile($jenkinsMasterHost+'/jnlpJars/agent.jar', $agentFile)
    }
    $proc = Start-Process -FilePath java -ArgumentList "-jar $agentFile -jnlpUrl $jenkinsMasterHost/computer/$curSlaveHost/jenkins-agent.jnlp -workDir $jenkinsDir"
    if($null -ne $proc) {
        $proc.WaitForExit()
    } else {
        exit $LASTEXITCODE
    }
}

SlaveSetup