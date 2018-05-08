-- 创建表
use xmp_data_mid;
drop table if exists highfun_test;
CREATE TABLE if not exists `highfun_test`(
  `day` string, 
  `cookieid` string,
  `pv` int
)
partitioned by (
    dtask string,
    dtype string
)
ROW FORMAT SERDE 
  'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe' 
WITH SERDEPROPERTIES ( 
  'field.delim'=',', 
  'serialization.format'=',') 
STORED AS INPUTFORMAT 
  'org.apache.hadoop.mapred.TextInputFormat' 
OUTPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat';

-- 数据加载
load data local inpath "highfun.txt"  overwrite into table highfun_test partition(dtask='analysis',dtype='rank');


-- 查询
--set hive.exec.mode.local.auto=true;
--SELECT 
--  cookieid,
--  createtime,
--  pv,
--  ROW_NUMBER() OVER(PARTITION BY cookieid ORDER BY pv desc) AS rn 
--FROM 
--    xmp_data_mid.highfun_test;
