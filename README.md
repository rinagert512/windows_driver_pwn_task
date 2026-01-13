В папке C:\Deploy файлы для разворачивания стенда
В папке C:\PwnServer файлы для поднятия сервера
Флаг в C:\flag.txt

Включить режим тестовой подписи
bcdedit /set testsigning on

И перезагрузить

С помощью psexec запустить сессию от имени nt authority\система:
.\PsExec64.exe -i -s powershell.exe 

Создать файл с флагом в C:\
echo "flag{congratulations_7351}" > flag.txt

Поменять SID владельца на NT AUTHORITY\СИСТЕМА
takeown /f .\flag.txt

Убрать наследованный DACL
icacls flag.txt /inheritance:r

Дать доступ только NT AUTHORITY\СИСТЕМА
icacls .\flag.txt /grant:r *S-1-5-18:F

Удалить PsExec64.exe, чтобы никто не абьюзил)

OSR Loader, выбрать драйвер, поставить ServiceStart = Automatic => Register Service + Start Service

С помощью nssm создаем сервис 
.\nssm.exe install PwnDriverServer "C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -ExecutionPolicy Bypass -File C:\PwnServer\server.ps1

.\nssm.exe set PwnDriverServer AppDirectory C:\PwnServer

.\nssm.exe set PwnDriverServer AppStdout   C:\PwnServer\stdout.log

.\nssm.exe set PwnDriverServer AppStderr   C:\PwnServer\stderr.log

.\nssm.exe set PwnDriverServer AppExit Default Restart

.\nssm.exe set  PwnDriverServer ObjectName .\user user

.\nssm.exe start PwnDriverServer

Копируем из C:\Windows\System32 ntoskrnl.exe

Для решения нужны файлы из папки to_participants
Сервер работает на порту 31337

В папке writeup решение задания (иногда не с первого раза выводит флаг, стоит несколько раз подряд ввести "3")
