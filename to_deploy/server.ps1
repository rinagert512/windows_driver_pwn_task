$log = 'C:\PwnServer\ps.log'
"[$(Get-Date)] script started" | Out-File $log -Append

$winsocat = 'C:\PwnServer\winsocat.exe'
$client   = 'C:\PwnServer\client.exe'
$listen   = "TCP-LISTEN:31337,reuseaddr,fork"
$exec     = "EXEC:'C:\PwnServer\client.exe'"

while ($true) {
    "[$(Get-Date)] starting winsocat" | Out-File $log -Append
    & $winsocat $listen $exec 2>&1 | Out-File $log -Append
    "[$(Get-Date)] winsocat exited, sleep" | Out-File $log -Append
    Start-Sleep -Seconds 2
}