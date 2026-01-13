# KStorage

## Описание

> Задание на использование примитивов `Arbitrary Read` и `Arbitrary Write` для повышения привилегий процесса.

В папке `C:\Deploy` файлы для разворачивания стенда
В папке `C:\PwnServer` файлы для поднятия сервера
Флаг в `C:\flag.txt`

В `pwn.pdf` описание задания и разбор его решения.

## Как разорачивать

1. Включить режим тестовой подписи
`bcdedit /set testsigning on`
И перезагрузить

2. С помощью `psexec` запустить сессию от имени `nt authority\система`:
`.\PsExec64.exe -i -s powershell.exe `

3. Создать файл с флагом в `C:\`
`echo "flag{congratulations_haha}" > flag.txt`

4. Поменять `SID` владельца на `NT AUTHORITY\СИСТЕМА`
`takeown /f .\flag.txt`

5. Убрать наследованный `DACL`
`icacls flag.txt /inheritance:r`

6. Дать доступ только `NT AUTHORITY\СИСТЕМА`
`icacls .\flag.txt /grant:r *S-1-5-18:F`

Удалить PsExec64.exe, чтобы никто не абьюзил)

7. OSR Loader, выбрать драйвер, поставить ServiceStart = Automatic => Register Service + Start Service

8. С помощью nssm создаем сервис 
```
.\nssm.exe install PwnDriverServer "C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -ExecutionPolicy Bypass -File C:\PwnServer\server.ps1
.\nssm.exe set PwnDriverServer AppDirectory C:\PwnServer
.\nssm.exe set PwnDriverServer AppStdout   C:\PwnServer\stdout.log
.\nssm.exe set PwnDriverServer AppStderr   C:\PwnServer\stderr.log
.\nssm.exe set PwnDriverServer AppExit Default Restart
.\nssm.exe set  PwnDriverServer ObjectName .\user user
.\nssm.exe start PwnDriverServer
```

9. Копируем из C:\Windows\System32 ntoskrnl.exe

## Что предоставить для решения
Для решения нужны файлы из папки to_participants
Сервер работает на порту 31337

В папке writeup решение задания (иногда не с первого раза выводит флаг, стоит несколько раз подряд ввести "3")

