-- 使用本地文件进行读取过滤，然后结果导出到本地
-- 2A5F8   [3,0,8] ["5486","0","0"]        0,1,0   124.91.9.111    1517673596
add file hive_streaming.sh;
add file ban_ver;
select transform(substr(fu1,2,5),fu2,fu5,fu7,fip,finsert_time)
using 'hive_streaming.sh'
as (pid,mlint,flstr,sstr,fip,ftime)
from xmp_odl.xmpplaydur where ds='20180204' limit 10;
