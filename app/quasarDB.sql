CREATE DATABASE IF NOT EXISTS quasarWebsite_db;
USE quasarWebsite_db;

DROP TABLE IF EXISTS quasarinfo;
DROP TABLE IF EXISTS quasarinfo_table2;
DROP TABLE IF EXISTS QuasarInfo;
DROP TABLE IF EXISTS QuasarInfo_table2;

CREATE TABLE quasarinfo(
    QSO VARCHAR(255) PRIMARY KEY,
    PLATE_MJD_FIBER VARCHAR(255) NOT NULL,
    ZEMDR9Q FLOAT NOT NULL,
    ZEMDR9Q_PM FLOAT,
    ZEMHW10 FLOAT,
    ZEMHW10_PM FLOAT,
    BALQSO VARCHAR(255) NOT NULL,
    GRAPH_IMG VARCHAR(255)
);

CREATE TABLE quasarinfo_table2(
    QSO VARCHAR(255),
    PLATE_MJD_FIBER VARCHAR(255) NOT NULL,
    BI_EHVO INT,
    V_max INT,
    V_min INT,
    EW INT,
    Depth FLOAT
);

-- https://www.tutorialspoint.com/how-to-get-the-datatype-of-mysql-table-columns#:~:text=You%20can%20get%20the%20MySQL,columns%E2%80%9D.&text=SELECT%20DATA_TYPE%20from%20INFORMATION_SCHEMA.,and%20table_name%20%3D%20'yourTableName'.
/*https://medium.com/@andrewpongco/solving-the-mysql-server-is-running-with-the-secure-file-priv-option-so-it-cannot-execute-this-d319de864285
//https://stackoverflow.com/questions/59993844/error-loading-local-data-is-disabled-this-must-be-enabled-on-both-the-client

//SHOW VARIABLES LIKE 'secure_file_priv';

//mysql --local-infile=1 -u root -p

// DROP TABLE quasarinfo
// SELECT * FROM quasarinfo; */

-- LOAD DATA LOCAL INFILE 'C:\Users\guine\Desktop\CapstoneResearch\table1.csv' 
-- INTO TABLE QuasarInfo
-- FIELDS TERMINATED BY ',' 
-- LINES TERMINATED BY '\n'
-- IGNORE 1 ROWS;
SET GLOBAL local_infile = true;

-- uncomment below for windows computers 

-- LOAD DATA LOCAL INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\table1.csv' 
-- INTO TABLE QuasarInfo
-- FIELDS TERMINATED BY ',' 
-- LINES TERMINATED BY '\r\n'
-- IGNORE 1 ROWS
-- (QSO, PLATE_MJD_FIBER, ZEMDR9Q, @vZEMDR9Q_PM, @vZEMHW10, @vZEMHW10_PM, BALQSO, GRAPH_IMG)
-- SET
-- ZEMDR9Q_PM = NULLIF(@vZEMDR9Q_PM, ''),
-- ZEMHW10 = NULLIF(@vZEMHW10, ''),
-- ZEMHW10_PM = NULLIF(@vZEMHW10_PM, '');

-- LOAD DATA LOCAL INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\table2.csv' 
-- INTO TABLE QuasarInfo_table2
-- FIELDS TERMINATED BY ',' 
-- LINES TERMINATED BY '\r\n'
-- IGNORE 1 ROWS;

--For school servers:

LOAD DATA LOCAL INFILE '/dw00/d18/guinek/QuasarResearchWebsite/app/csv_tables/table1.csv' 
INTO TABLE quasarinfo
FIELDS TERMINATED BY ',' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(QSO, PLATE_MJD_FIBER, ZEMDR9Q, @vZEMDR9Q_PM, @vZEMHW10, @vZEMHW10_PM, BALQSO, GRAPH_IMG)
SET
ZEMDR9Q_PM = NULLIF(@vZEMDR9Q_PM, ''),
ZEMHW10 = NULLIF(@vZEMHW10, ''),
ZEMHW10_PM = NULLIF(@vZEMHW10_PM, '');

LOAD DATA LOCAL INFILE '/dw00/d18/guinek/QuasarResearchWebsite/app/csv_tables/table2.csv' 
INTO TABLE quasarinfo_table2
FIELDS TERMINATED BY ',' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;


-- INSERT INTO quasarinfo(Graph_Images) 
-- VALUES (LOAD_FILE('C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\spec-3655-55240-0388_Fig40.pdf'))
-- WHERE PLATE_MJD_FIBER = '3655-55240-0388'

-- UPDATE quasarinfo
-- SET quasarinfo.Graph_Images =LOAD_FILE('C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\spec-3655-55240-0388_Fig40.pdf')
-- WHERE PLATE_MJD_FIBER = 3655-55240-0388;