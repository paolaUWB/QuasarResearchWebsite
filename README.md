# ReadMe

## Hosting on UW Shared Host Servers

### Necessary software:
* Cyberduck (https://cyberduck.io/), or whatever secure file transfer software you prefer
* Putty (if on windows)
* SSH (if on Mac or Linux)

### Instructions:
1. Activate your UW shared web hosting.
    1. Follow instructions at https://itconnect.uw.edu/connect/web-publishing/shared-hosting/activating-shared-web-hosting/
        1. If you are a student, your server is Vergil
        1. If you are faculty, your server is Homer/Ovid
        
1. Download website files (if you haven't already done so) at: https://github.com/Kathleen-G/QuasarResearchWebsite

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
        1. Voila! You should be in now! Check that everything worked by typing `ls` into the command prompt. You should see two directories, "public_html" and "local_home"
        
    1. If you need more information, see https://itconnect.uw.edu/connect/web-publishing/shared-hosting/ssh/
 
 1. Set up a python virtual environment: 
     1. `cd ~/public_html`
     1. type into the prompt:
         1. `python3 -m venv flaskEnv` (this will take a couple of seconds to run)
         1. `source flaskEnv/bin/activate` You should now see something like: `(flaskEnv) vergil11$`
         1. `pip install flask`
         1. `deactivate`
         
 1. Add files to the web server
     1. In the terminal create a new file directory to hold the website files with the following commands:
         1. `cd ~/public_html`
         1. `mkdir ResearchWebsite`
     1. Open Cyberduck
         1. Open Connection (use the same credentials as Putty)
     1. Click and drag the 'app' folder from your computer files into the 'ResearchWebsite' folder on cyberduck
    
 
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
         1. First, let's copy down the absolute path to our python virtual environment
             1. `cd ~/public_html`
             1. `pwd flaskEnv`
                 1. copy this into a notepad file or whatever program you want (we'll need this for the next step)
         1. Type `pico main.cgi' into the terminal
         1. In this file, type the following (be careful!)
             ```
             #!/usr/local/bin/python3.6
             import sys, os
             import cgi;
             import cgitb; cgitb.enable()
             from wsgiref.handlers import CGIHandler

             sys.path.insert(0, '<THE_FILE_PATH_YOU_COPIED_DOWN>/flaskEnv/lib/python3.6/site-packages')

             from ResearchWebsite.app.__init__ import app

             CGIHandler().run(app)
             ```
             Your sys.path. insert file should look something like this: `/nfs/bronfs/uwfs/da00/d18/guinek/flaskEnv/lib/python3.6/site-packages`
             It's super important that you have the preceding backslash in front (or else nothing works). Your import line (`from ResearchWebsite.app.__init__ import app`)       should reflect the path from your public_html folder to your __init__.py file in the flask project. 
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
         

 
