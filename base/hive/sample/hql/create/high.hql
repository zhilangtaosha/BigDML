use xmp_data_mid;
drop table if exists high_test;
create table if not exists high_test(
   id string,
   s1 string,
   s2 string,
   s3 string,
   s4 string,
   a1 array<string>,
   a2 array<int>,
   m1 map<string,string>,
   m2 map<string,int>,
   n1 int,
   n2 int)
partitioned by (dtask string)
row format delimited
fields terminated by '\t'
COLLECTION ITEMS TERMINATED BY ','
map keys terminated by ':'
stored as textfile;




--set hive.exec.mode.local.auto=true; 
--set hive.exec.mode.local.auto.inputbytes.max=50000000;
--set hive.exec.mode.local.auto.tasks.max=10;

--数据加载
load data local inpath "high.txt"  overwrite into table high_test partition(dtask='analysis');


