# ReadMe

## Hosting on UW Shared Host Servers

### Necessary software:
* Github account with access to this github page
* Putty (if on windows)
* SSH (if on Mac or Linux)

### Instructions for school server setup:
1. Activate your UW shared web hosting.
    1. Follow instructions at https://itconnect.uw.edu/connect/web-publishing/shared-hosting/activating-shared-web-hosting/
        1. If you are a student, your server is Vergil
        1. If you are faculty, your server is Homer/Ovid
        

1. SSH into the school servers:
    1. If you are on Windows, open Putty
    1. Under Host Name put "vergil.u.washington.edu"
        1. Port 22
        1. Connection type SSH
        1. Under Saved Sessions type whatever name you want
        1. click "Save" (this will make it so that you can just double click or load next time you want to access the server)
        1. click Open
        1. Login as: `Your UW ID`
        1. Password: `Your UW password`
            1. If you are new to SSH, know that you won't actually see your password get typed. It'll look invisible but it is still getting input into the system.
        1. Voila! You should be in now! Check that everything worked by typing `ls` into the command prompt. You should see one directory, "public_html"
        
    1. If you need more information, see https://itconnect.uw.edu/connect/web-publishing/shared-hosting/ssh/
 
 1. Setup MySQL on the school servers:
    1. Follow directions at: https://itconnect.uw.edu/connect/web-publishing/shared-hosting/using-mysql-on-shared-uw-hosting/install-mysql/
    1. Make sure to write down your root password and username
             
 1. Add files to the web server
     1. In the terminal clone files from github with the following commands:
         1. `cd ~/public_html`
         1. `git clone https://<YOUR_GITHUB_USERNAME>@github.com/Kathleen-G/QuasarResearchWebsite.git`
         1. Enter your github password when prompted
         
     1. Check to see if all of the files were cloned
         1. `ls`
         1. You should see a new "QuasarResearchWebsite" directory in your public_html folder 
    
 1. Set up a python virtual environment: 
     1. `cd ~/public_html`
     1. type into the prompt:
         1. `python3 -m venv flaskEnv` (this will take a couple of seconds to run)
         1. `source flaskEnv/bin/activate` You should now see something like: `(flaskEnv) vergil11$`
         1. `pip install flask`
         1. `pip install PyMySQL`
         1. `pip install Flask-WTF`
         1. `pip install python-dotenv`
         
 1. create a .env file to store secret information
     1. `cd ~/public_html/QuasarResearchWebsite`
     1. `nano .env`
     1. type the following: 
        ```
        SECRET_KEY= <WHATEVER_SECRET_KEY_YOU_WANT>
        MYSQL_DATABASE_PASSWORD=<YOUR_MYSQL_DATABASE_ROOT_PASSWORD>
        MYSQL_DATABASE_PORT = <YOUR_MYSQL_DATABASE_PORT>
            
        ```
     1. Save and close with the following commands:
         ```
         ctrl+x
         y
         enter
         ```
         
 1. Setup DB
     1. `cd ~/public_html/QuasarResearchWebsite/app`
     1. Create and update the database with the following command (it will run the commands in the .sql file) `~/mysql/bin/mysql < quasarDB.sql -u root -p --verbose`  
     1. Update DB with graph images
         1. `cd ~/public_html/QuasarResearchWebsite/app`
         1. `python updateDatabase.py`
     
 1. Edit htaccess and cgi files
     1. This next part is a little tricky and easy to make a mistake by leaving off slashes by accident. Be careful here!
     1. Make sure you are in your 'public_html' directory `cd ~/public_html`
     1. In the terminal create a new htaccess file by typing the following: `pico .htaccess`
         1. Enter the following into the file:
             ```
             RewriteEngine on
             
             RewriteRule ^/?$ /<YOUR_UW_NETID>/main.cgi [L]
             ```
         1. Save and close with the following commands:
             ```
             ctrl+x
             y
             enter
             ```
     1. Now we need to create the CGI file
         1. `cd ~/public_html`

         1. Type `pico main.cgi' into the terminal
         1. Copy and paste this into the file (you can paste in Putty by clicking left and right mouse buttons at the same time) 
             ```

            #!flaskEnv/bin/python3

            import sys, os
            import cgi;
            import cgitb; cgitb.enable()
            from wsgiref.handlers import CGIHandler

            sys.path.insert(0, 'QuasarResearchWebsite')
            sys.path.insert(0, 'QuasarResearchWebsite/app')

            from app.__init__ import app
            CGIHandler().run(app)

             ```

         1. Save and close with:
             ```
             ctrl+x
             y
             enter
             ```
          1. Change the file permissions to allow the server to execute the program with `chmod 755 main.cgi`
          1. Now change the file permissions for the python init file with the following commands: 
              1. `cd ~/public_html/ResearchWebsite/app`
              1. `chmod 755 __init__.py`
              
     1. Check to see if it worked by going to your UW url. It will be https://students.washington.edu/<YOUR_UW_NETID>/
    
## Instructions for local setup (Windows):
    
1. Install MySQL https://dev.mysql.com/downloads/installer/ (install the second option useing all default options)
    
1. Install visual studio code https://code.visualstudio.com/ (or whatever your preferred IDE is)
    
1. Install Git if you don't already have it: https://git-scm.com/download/win
         
1. Clone this repository 
     1. Open the command prompt
     1. cd to whatever folder you want to have the project in 
     1. `git clone https://<YOUR_GITHUB_USERNAME>@github.com/Kathleen-G/QuasarResearchWebsite.git`
         
1. Check to see if all of the files were cloned
     1. `dir`
     1. You should see a new "QuasarResearchWebsite" directory
         
1. Open project in visual studio code
     1. Open visual studio code
     1. File -> Open folder and then navigate to the QuasarResearchWebsite folder that you just cloned
         
1. Set up flask environment:
     1. Open a new terminal in visual studio
     1. In the terminal `python3 -m venv flaskEnv` (this will take a couple of seconds to run)
     1. `flaskEnv/Scripts/activate` You should now see something like: `(flaskEnv) PS C:\Users\guine\Desktop\test\QuasarResearchWebsite> `
         1. You may recieve an error message stating "running scripts is disabled on this system"
         1. To fix this open Windows PowerShell with administration privileges
             1. To open, search "PowerShell" in the Windows Start menu and select "Run as administrator" from the context menu
         1. Enter 'set-executionpolicy remotesigned' to PowerShell
         1. When asked "Do you want to change the execution policy?", respond with 'Y' for yes
     1. `pip install flask`
     1. `pip install PyMySQL`
     1. `pip install Flask-WTF`
     1. `pip install python-dotenv`
         
     1. For more instructions on using python environments in visual studio, see https://code.visualstudio.com/docs/python/environments
     
1. Add the secret environment variables:
    1. Create a new file in QuasarResearchWebsite/app/  and name it .env
    1. Add your secrets to the file with the following: 
    ```
    SECRET_KEY=<WHATEVER YOU WANT>
    MYSQL_DATABASE_PASSWORD=<YOUR MYSQL DB/ROOT PASSWORD>
    ```
    
1. Setup the MySQL database:
    1. In the VSCode command line, start mysql with `& cmd.exe /c "mysql -u root -p --verbose --local-infile=1 < app/quasarDB_win.sql"`, and enter your password for root user
    1. `python app/updateDatabase_win.py` (this will update the paths to the images in the database)
    
1. Now check to see if things are working. In the visual studio terminal type `flask run` 
    1. If everything is working you should see something like:
        ```
        (flaskEnv) PS C:\Users\guine\Desktop\test\QuasarResearchWebsite> flask run
        * Environment: production
        WARNING: This is a development server. Do not use it in a production deployment.
        Use a production WSGI server instead.
        * Debug mode: off
        * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
        ```
    1. Follow the link on the last line to see if it runs. Your default internet browser should open to the home page of the website. 
    1. Check that the images are loading correctly by going to the "Data Access" page, clicking on a row and seeing if the image shows up.
    1. Voila! Hopefully it is working :)
    
   ## Troubleshooting (Windows):
   1. To update and access most recent files enter 'git pull' into the terminal when you are in your QuasarResearchWebsite folder
             
   1. If you recieve the error message: "running scripts is disabled on this system"
         1. Open Windows PowerShell with administration privileges
             1. To open, search "PowerShell" in the Windows Start menu and select "Run as administrator" from the context menu
         1. Enter 'set-executionpolicy remotesigned' to PowerShell
         1. When asked "Do you want to change the execution policy?", respond with 'Y' for yes  
         
   1. To add the mysql exe file to the path
         1. type "path" into the windows search bar and click "edit the system environment variables"
         1. click on environment variables
         1. click on path, then edit, then new
         1. then add the path 'C:\Program Files\MySQL\MySQL Shell 8.0\bin\' to the list 
         1. click ok/apply
         1. restart your computer



 
