# 创建表
# 文本格式存储
use kankan_odl;drop table if exists hive_table_templete;
create external table if not exists hive_table_templete(
  subid int,
  peerid string,
  movieid int)
partitioned by (ds string)
row format delimited
fields terminated by '\t'
stored as textfile;

# 序列化格式存储
use kankan_odl;drop table if exists hive_table_templete;
create external table if not exists union_install(
   Fu1 string,
   Fu2 string,
   Fu3 string,
   Fu4 string,
   Fu5 string,
   Fu6 string,
   Fu7 string,
   Fu8 string,
   Fu9 string,
   Fip string,
   Finsert_time int,
   isp string
  )
partitioned by (ds string,hour string)
row format delimited
fields terminated by '\u0001'
stored as inputformat
  'org.apache.hadoop.mapred.SequenceFileInputFormat'
outputformat
  'org.apache.hadoop.hive.ql.io.HiveSequenceFileOutputFormat';



# 导入数据
ihql="use kankan_odl;delete from tbname where ds='${date}';load data local inpath '/home/work/test.txt' into table tbname;"
${HIVE} -e "${chql}"

# 导出数据
esql="use kankan_odl;select '${date}',fu3,fu2,count(*) from xmpcloud2 where ds='${date}' and length(fu4)=16 group by fu3,fu2;"
${HIVE} -e "${esql}" > $datapath/xmp_cloud_${date}



# 导出数据到本地文件(并指定字段分割方式)
insert overwrite local directory '/tmp/xx' row format delimited fields terminated by '\t' select * from test;

# hive写本地数据
insert overwrite local directory '/data/access_log/access_log.45491' row format delimited fields terminated by ' ' collection items terminated by ' ' select *

# hive修改表的存储属性
alter TABLE  pusherdc   SET FILEFORMAT
INPUTFORMAT "org.apache.hadoop.mapred.SequenceFileInputFormat"
OUTPUTFORMAT "org.apache.hadoop.hive.ql.io.HiveSequenceFileOutputFormat";

# hive显示分区
use xmp_odl;show partitions $tbl partition(ds='$date');

# hive添加分区
use xmp_odl;alter table $tbl add if not exists partition (ds='$date',hour='$hour');

# hive删除分区
use xmp_odl;alter table $tbl drop partition(ds='20160808',hour='00');

# hive修改分区
use xmp_odl;alter table $tbl partition(ds='20160808',hour='00') set location "/user/kankan/warehouse/..."
use xmp_odl;alter table $tbl partition(ds='20160808',hour='00') rename to partition(ds='20160808',hour='01')


# hive添加列
use xmp_odl;alter table $tbl add columns(col_name string);

# hive修改列
use xmp_odl;alter table $tbl change col_name newcol_name string [after x] [first];

# hive表重命名
use xmp_odl;alter table $tbl rename to new_tbl_name;