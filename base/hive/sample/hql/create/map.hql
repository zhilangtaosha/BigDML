-- 创建
CREATE TABLE `map_test`(
  `a` string, 
  `b` map<string,string>, 
  `c` string)
ROW FORMAT SERDE 
  'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe' 
WITH SERDEPROPERTIES ( 
  'colelction.delim'=',', 
  'field.delim'='\t', 
  'mapkey.delim'=':', 
  'serialization.format'='\t') 
STORED AS INPUTFORMAT 
  'org.apache.hadoop.mapred.TextInputFormat' 
OUTPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat';


-- map数据导入
use xmp_data_mid;
load data local inpath 'map.txt' into table map_test;

-- 数据查询
select b['b1'],get_json_object(c,'$.c1') from map_test;
select nvl(b['b1'],0),nvl(get_json_object(c,'$.c1'),0) from map_test;
