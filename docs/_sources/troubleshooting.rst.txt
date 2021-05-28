Troubleshooting
===============

Troubleshooting (School Server)
--------------------------------

1. Basic MySQL Administration:
   https://itconnect.uw.edu/connect/web-publishing/shared-hosting/using-mysql-on-shared-uw-hosting/basic-mysql-administration/

2. Troubleshooting Steps:
   https://itconnect.uw.edu/connect/web-publishing/shared-hosting/troubleshooting/

3. If the Data Access page doesn't work (E.g. "Internal Server Error",
   data not displaying, etc.) 1. Go to **init**.py 1. Change the port
   number in the method connect\_db() to have your port number

Troubleshooting (Windows)
--------------------------

1. To update and access most recent files enter ``git pull`` into the
   terminal when you are in your QuasarResearchWebsite folder

2. To push your most recent files to the master branch 1. Enter
   ``git status`` to list out files that have been added/changed. the
   names of the files should be red 1. Add files that are unecessary to
   the project to .gitignore 1. Enter ``git status`` To list out files
   again to check if those files were removed. 1. Enter ``git add .`` To
   the terminal. 1. Enter ``git status`` to the terminal. The names of
   the files should now be green. 1. Enter git ``commit -m "message"``.
   You can change the message to anything you want but it should be
   somewhat descriptive. 1. Enter git \`push to the terminal. 1. If this
   is your first time doing so you should type in "git push
   --set-upstream origin YourBranch". Change "YourBranch" to the actual
   name of the branch. 1. Go to the Github repository to merge your
   request

3. If you recieve the error message: "running scripts is disabled on this system" 
   1. Open Windows PowerShell with administration privileges 
   1. To open, search "PowerShell" in the Windows Start menu and select "Run as administrator" from the context menu 
   1. Enter ``set-executionpolicy remotesigned`` to PowerShell 
   1. When asked "Do you want to change the execution policy?", respond with ``Y`` for yes 
   1. For more information visit: https://www.faqforge.com/windows/windows-powershell-running-scripts-is-disabled-on-this-system/

4. To add the mysql exe file to the path 1. type "path" into the windows
   search bar and click "edit the system environment variables" 1. click
   on environment variables 1. click on path, then edit, then new 1.
   then add the paths ``C:\Program Files\MySQL\MySQL Shell 8.0\bin\``
   and ``C:\Program Files\MySQL\MySQL Server 8.0\bin\`` to the list 1.
   click ok/apply 1. restart your computer

   1. If you recieve the error mesage: ``module not found``

      1. Type ``python -m pip list`` into VS Code's terminal
      2. This will list all installed packages
      3. If the package you need is not in the list, enter
         ``pip install [package name]`` to the terminal

         1. For example, if you need to install PyMySql, enter
            ``pip install PyMySQL`` to the terminal

   2. Setting the virtual enviroment in VS Code

      1. type "path" into the windows search bar and click "edit the
         system environment variables"
      2. Use ``CTRL + SHIFT + P``
      3. click on "Python: select interpreter"
      4. Select the path that has flaskEnv/Scripts/ in the path name
      5. To learn more check this page:
         https://code.visualstudio.com/docs/python/environments
         