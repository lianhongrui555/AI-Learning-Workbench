param(
    # 测试时可以只启动服务而不要打开浏览器。
    [switch]$NoBrowser
)

# 项目根目录：当前脚本位于 scripts 目录下。
$projectDir = Split-Path -Parent $PSScriptRoot
$appPath = Join-Path $projectDir 'app.py'

# 优先使用项目虚拟环境；没有虚拟环境时使用系统 Python。
$venvPython = Join-Path $projectDir '.venv\Scripts\python.exe'
$python = if (Test-Path -LiteralPath $venvPython) { $venvPython } else { 'D:\python\python.exe' }

# 工作台地址和本地健康检查地址。
$url = 'http://127.0.0.1:5000/'
$healthUrl = 'http://127.0.0.1:5000/health'

function Test-WorkbenchReady {
    try {
        $response = Invoke-WebRequest -Uri $healthUrl -UseBasicParsing -TimeoutSec 2
        return $response.StatusCode -eq 200
    } catch {
        return $false
    }
}

# 如果服务已经运行，直接打开浏览器。
if (-not (Test-WorkbenchReady)) {
    $outLog = Join-Path $env:TEMP 'ai-learning-workbench.out.log'
    $errLog = Join-Path $env:TEMP 'ai-learning-workbench.err.log'
    Start-Process -FilePath $python -ArgumentList @('-X', 'utf8', $appPath) -WorkingDirectory $projectDir -WindowStyle Hidden -RedirectStandardOutput $outLog -RedirectStandardError $errLog | Out-Null

    # 最多等待 30 秒，让 Flask 完成启动。
    $ready = $false
    for ($i = 0; $i -lt 30; $i++) {
        Start-Sleep -Seconds 1
        if (Test-WorkbenchReady) {
            $ready = $true
            break
        }
    }

    if (-not $ready) {
        Add-Type -AssemblyName PresentationFramework -ErrorAction SilentlyContinue
        [System.Windows.MessageBox]::Show(
            "工作台启动失败。`n`n请检查 Docker、Ollama 和项目依赖。`n错误日志：$errLog",
            'AI 学习工作台',
            'OK',
            'Error'
        ) | Out-Null
        exit 1
    }
}

if (-not $NoBrowser) {
    Start-Process $url
}