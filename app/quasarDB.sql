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

SET GLOBAL local_infile = true;

LOAD DATA LOCAL INFILE 'csv_tables/table1.csv' 
INTO TABLE quasarinfo
FIELDS TERMINATED BY ',' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(QSO, PLATE_MJD_FIBER, ZEMDR9Q, @vZEMDR9Q_PM, @vZEMHW10, @vZEMHW10_PM, BALQSO, GRAPH_IMG)
SET
ZEMDR9Q_PM = NULLIF(@vZEMDR9Q_PM, ''),
ZEMHW10 = NULLIF(@vZEMHW10, ''),
ZEMHW10_PM = NULLIF(@vZEMHW10_PM, '');

LOAD DATA LOCAL INFILE 'csv_tables/table2.csv' 
INTO TABLE quasarinfo_table2
FIELDS TERMINATED BY ',' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

SELECT PLATE_MJD_FIBER,
  substr(PLATE_MJD_FIBER, 1, length(PLATE_MJD_FIBER) - length(substring_index(PLATE_MJD_FIBER, '-', -2))) PLATE,
  substring_index(substring_index(addr, '-', -2), '-', 1) MJD,
  substr(trim(substring_index(addr, '-', -1)),1,2) FIBER,
FROM quasarinfo

SELECT PLATE_MJD_FIBER,
  substr(PLATE_MJD_FIBER, 1, length(PLATE_MJD_FIBER) - length(substring_index(PLATE_MJD_FIBER, '-', -2))) PLATE,
  substring_index(substring_index(addr, '-', -2), '-', 1) MJD,
  substr(trim(substring_index(addr, '-', -1)),1,2) FIBER,
FROM quasarinfo2