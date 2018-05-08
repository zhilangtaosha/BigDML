use xmp_data_mid;
CREATE TABLE if not exists winana(
    month STRING,
    day STRING, 
    cookieid STRING )
ROW FORMAT DELIMITED 
FIELDS TERMINATED BY ',' 
stored as textfile;
