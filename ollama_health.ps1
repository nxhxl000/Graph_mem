Write-Host 'Ollama health check...'

try {
     = Invoke-WebRequest -Uri 'http://localhost:11434' -Method GET -UseBasicParsing
    Write-Host 'Ollama работает!'
}
catch {
    Write-Host 'Ollama НЕ отвечает!'
}
