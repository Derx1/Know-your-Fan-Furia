# Este script cria uma tarefa agendada para manter o aplicativo Flask rodando
# Deve ser executado como Administrador

$taskName = "FURIA Know Your Fan App"
$taskDescription = "Mantém o aplicativo web Flask rodando"
$workingDir = $PSScriptRoot
$scriptPath = Join-Path $workingDir "run_app.bat"

# Caminho para o executável do Python
$pythonPath = "python.exe"

# Criar a ação para a tarefa
$action = New-ScheduledTaskAction -Execute $scriptPath -WorkingDirectory $workingDir

# Configurar para iniciar com o Windows
$trigger = New-ScheduledTaskTrigger -AtStartup

# Configurar as configurações
$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -ExecutionTimeLimit (New-TimeSpan -Days 365)

# Obter as informações de usuário atual
$currentUser = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name

# Verificar se a tarefa já existe
$existingTask = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue

if ($existingTask) {
    # Remover tarefa existente
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
    Write-Host "Tarefa existente removida."
}

# Registrar a nova tarefa
Register-ScheduledTask `
    -TaskName $taskName `
    -Action $action `
    -Trigger $trigger `
    -Settings $settings `
    -Description $taskDescription `
    -User $currentUser `
    -RunLevel Highest

# Iniciando a tarefa imediatamente
Start-ScheduledTask -TaskName $taskName

Write-Host "Tarefa agendada '$taskName' criada e iniciada com sucesso!"
Write-Host "O aplicativo web Flask agora será iniciado automaticamente com o Windows e continuará rodando em segundo plano."