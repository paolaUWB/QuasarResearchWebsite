
import os
import pymysql
from dotenv import load_dotenv

load_dotenv()

def connect_db():
    pwd = os.environ.get('MYSQL_DATABASE_PASSWORD')

    return pymysql.connect(
        host = 'localhost', user = 'root', password = os.environ.get('MYSQL_DATABASE_PASSWORD'),
        database = 'test', autocommit = True, charset = 'utf8mb4',
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

directory = r'/dw00/d18/guinek/QuasarResearchWebsite/app/static/images'
for entry in os.scandir(directory):
    if entry.path.endswith(".pdf") and entry.is_file():
        fileName = "'images/Graph_Images/" + entry.name + "'"
        QusasarMDJ = entry.name[5:-10]
        sql = ("UPDATE quasarinfo SET " 
            "quasarinfo.GRAPH_IMG = %s WHERE trim(PLATE_MJD_FIBER) = \"%s\";" % (fileName, QusasarMDJ))
        print(sql + "\n")
        cursor.execute(sql)
