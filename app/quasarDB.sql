 DROP TABLE quasarinfo;

 CREATE TABLE QuasarInfo(
    QSO VARCHAR(255) PRIMARY KEY,
    PLATE_MJD_FIBER VARCHAR(255) NOT NULL,
    ZEMDR9Q FLOAT NOT NULL,
    ZEMDR9Q_PM FLOAT,
    ZEMHW10 FLOAT,
    ZEMHW10_PM FLOAT,
    BALQSO VARCHAR(255) NOT NULL
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

LOAD DATA LOCAL INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\table1.csv' 
INTO TABLE QuasarInfo
FIELDS TERMINATED BY ',' 
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS;