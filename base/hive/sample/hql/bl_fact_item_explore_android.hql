use xmp_data_mid;
CREATE TABLE if not exists  `bl_fact_item_explore_android`(
  `guid` string, 
  `phonetype` string, 
  `channelid` string, 
  `ip` string, 
  `sessionid` string, 
  `network` string, 
  `version` string, 
  `userid` string, 
  `movieid` string, 
  `model` string, 
  `sab` string, 
  `rsessionid` string, 
  `rn` string, 
  `refreshid` string, 
  `position` string, 
  `refreshnum` string, 
  `ts` bigint, 
  `ownerid` string, 
  `owner_type` string, 
  `video_type` string, 
  `duration` string, 
  `retype` string, 
  `source` string)
PARTITIONED BY ( 
  `ds` string, 
  `page` string, 
  `card` string)
ROW FORMAT SERDE 
  'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe' 
WITH SERDEPROPERTIES ( 
  'colelction.delim'=',', 
  'field.delim'='\t', 
  'mapkey.delim'=':', 
  'serialization.format'='\t');
