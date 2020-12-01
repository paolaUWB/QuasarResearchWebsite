
import os
import pymysql
from dotenv import load_dotenv

load_dotenv()

def connect_db():
    pwd = os.environ.get('MYSQL_DATABASE_PASSWORD')

    return pymysql.connect(
        host = 'vergil.u.washington.edu', user = 'root', password = os.environ.get('MYSQL_DATABASE_PASSWORD'),
        database = 'quasarWebsite_db', autocommit = True, charset = 'utf8mb4', port= int(os.environ.get('MYSQL_DATABASE_PORT')),
        cursorclass = pymysql.cursors.DictCursor) 

cursor = connect_db().cursor()


#add blob pdfs to database
# directory = r'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\Graph images'
# for entry in os.scandir(directory):
#     if entry.path.endswith(".pdf") and entry.is_file():
#         filenammm = entry.name

#         fileName = "C:\\\\ProgramData\\\\MySQL\\\\MySQL Server 8.0\\\\Uploads\\\\Graph images\\\\" + entry.name
#         QusasarMDJ = entry.name[5:-10]
#         sql = ("UPDATE quasarinfo SET " 
#             "quasarinfo.Graph_Images = LOAD_FILE('%s') WHERE trim(PLATE_MJD_FIBER) = \"%s\";" % (fileName, QusasarMDJ))
#         cursor.execute(sql)


#add file locations to

basedir = os.path.abspath(os.path.dirname(__file__))
GRAPH_IMAGES = os.path.join(basedir, 'static/images/Graph_Images')
directory = GRAPH_IMAGES
for entry in os.scandir(directory):
    #print(entry.path)
    if entry.path.endswith(".pdf") and entry.is_file():
        fileName = "'images/Graph_Images/" + entry.name + "'"
        QusasarMDJ = entry.name[5:-10]
        sql = ("UPDATE quasarinfo SET " 
            "quasarinfo.GRAPH_IMG = %s WHERE trim(PLATE_MJD_FIBER) = \"%s\";" % (fileName, QusasarMDJ))
        #print(sql + "\n")
        cursor.execute(sql)
