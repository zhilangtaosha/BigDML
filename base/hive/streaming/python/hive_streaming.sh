#!/bin/bash
dir=`dirname $0` && dir=`cd $dir && pwd`
source /usr/local/sandai/server/bin/common/global_var.sh
cd $dir

datapath=${dir/\/bin/\/data}
[ ! -d $datapath ]&&mkdir -p $datapath

date=$1
[ -z $date ]&&date=`date -d "-1 day" +%Y%m%d`
echo "CalcDay:"$date


# 直接写入表
function write_table()
{
	local hql="${UDFLIB};${UDF_CREATE};
		add file hive_streaming.py;
		from(select fu1 as pid,fu2 as lint,fu5 as lstr,fu7 as sstr,fip,finsert_time as fs from xmp_odl.xmpplaydur where ds='$date' cluster by fip)a
		insert overwrite table xmp_data_mid.streaming_test partition(ds='${date}')
		reduce a.pid,a.lint,a.lstr,a.sstr,a.fip,a.fs
		using 'hive_streaming.py'
		as pid,mlint,flstr,sstr,fip,ftime;
		"

	echo "$hql"
	${HIVE} -e "$hql"
}

# 直接写入本地文件（注意此处的limit 1000是过滤后的1000条，而不是先取1000条再过滤）
function write_local()
{
    local hql="
        add file hive_streaming.py;
        select transform(substr(fu1,2,5),fu2,fu5,fu7,fip,finsert_time)
        using 'hive_streaming.py'
        as (pid,mlint,flstr,sstr,fip,ftime)
        from xmp_odl.xmpplaydur where ds='$date' limit 1000;
    "
    echo "$hql"
    ${HIVE} -e "$hql" > streaming_proc

    return 0
}


# 测试入口
write_table
write_local


exit 0
