use xmp_data_mid;
drop table if exists streaming_test;
create table if not exists streaming_test(
   pid string,
   mlint string,
   flstr string,
   sstr string,
   fip string,
   ftime string
  )
partitioned by (ds string)
row format delimited
fields terminated by '\t'
stored as inputformat
  'org.apache.hadoop.mapred.SequenceFileInputFormat'
outputformat
  'org.apache.hadoop.hive.ql.io.HiveSequenceFileOutputFormat';