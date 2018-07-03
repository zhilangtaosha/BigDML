-- 创建表
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


--在此基础上的函数测试
select percentile_approx(a2[1],array(0.25,0.5,0.75)) from high_test;

select percentile_approx(num,array(0.25,0.5,0.75)) 
from 
(
    select a2[1] as num from high_test order by num
)a;



