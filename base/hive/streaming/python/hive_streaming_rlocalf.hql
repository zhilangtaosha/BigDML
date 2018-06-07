-- 使用本地文件进行读取过滤，然后结果导出到本地
add file hive_streaming_local.py;
add file ban_ver;
select transform(substr(fu1,2,5),fu2,fu5,fu7,fip,finsert_time)
using 'hive_streaming_localf.py'
as (pid,mlint,flstr,sstr,fip,ftime)
from xmp_odl.xmpplaydur where ds='20180204' limit 10;
