-- 创建表
use xmp_data_mid;
drop table if exists tbl_a;
create table if not exists tbl_a(
   id string,
   s1 string,
   n1 int)
partitioned by (dtask string)
row format delimited
fields terminated by '\t'
collection items terminated by ','
map keys terminated by ':'
stored as textfile;



drop table if exists tbl_b;
create table if not exists tbl_b(
   id string,
   s1 string,
   n1 int)
partitioned by (dtask string)
row format delimited
fields terminated by '\t'
collection items terminated by ','
map keys terminated by ':'
stored as textfile;



-- 加载数据
load data local inpath "tjoin_a.txt"  overwrite into table tbl_a partition(dtask='tjoin');
load data local inpath "tjoin_a.txt"  overwrite into table tbl_b partition(dtask='tjoin');


-- 查询测试(并没有交叉积的情况产生)
set hive.exec.mode.local.auto=true;
use xmp_data_mid;
select ta.*,tb.* from tbl_a ta inner join tbl_b tb on ta.id=tb.id;