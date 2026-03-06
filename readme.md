<h1 align="center">Nipy</h1>

# Что это? / who is tha
  Это установщик приложений который может подтягивать сами инсталлеры прямо с вашей SFTP/FTP/FTPS сети.
  
  Концепт взят с [Ninite](https://ninite.com/)

  ## Для кого это расчитано? 
  > на юзеров которые часто переустанавливают систему но при этом имеют FTP* сервер с которого можно выкачать файлы
> 
> FTP* - все что подразумевает под собой file transfer protocol aka ftp / sftp / ftps
> 

# How to build for yourself
  Что бы собрать App Installer омг нужно :
  ```
  pip install pyinstaller
  ```

  
  ```
  pip install scp
  ```
  ```
  pip install paramiko
  ```
  ```  
  pip install customtkinter
  ```
  и наконец 
  ```
  pyinstaller --onefile --noconsole --collect-all customtkinter AppInstaller/main.py
  ```

> [!TIP]
> Что бы установщик у вас работал, нужно заглянуть в main.py и отредактировать секцию конфигурации т.к все там заменено на бланк
>

> [!NOTE]
> На данный момент добавление приложений для инсталляции доступно только через редактированние секции APPS = []

