##Hive-Streaming
[TOC]

### 基础

#### 原理

mapper和reducer会从标准输入中读取用户数据，一行一行处理后发送给标准输出。Streaming工具会创建MapReduce作业，发送给各个tasktracker，同时监控整个作业的执行过程。

如果一个文件（可执行或者脚本）作为mapper:

- mapper初始化时，每一个mapper任务会把该文件作为一个单独进程启动，
- mapper任务运行时，它把输入切分成行并把每一行提供给可执行文件进程的标准输入。 同时，mapper收集可执行文件进程标准输出的内容，并把收到的每一行内容转化成key/value对，作为mapper的输出。 默认情况下，一行中第一个tab之前的部分作为`key`，之后的（不包括tab）作为`value`。如果没有tab，整行作为key值，value值为null。

对于reducer，类似

以上是Map/Reduce框架和streaming mapper/reducer之间的基本通信协议。

### 实现

streaming的实现可以用多种语言，此处挑选python,c,shell,perl来实现

#### python

调用的python文件需要使用到第三方文件该如何处理

标准示例：

```mysql
select 
	transform(uid,mid,rating,utime) 
using 'python weekday.py' 
as (uid,mid,rating,weekday) 
from rating;
```

##### 插入到表

方法1：

```shell
# t_stat_url_upload_split.sh

add file t_stat_url_upload_split_mapper.py;
from(
	select 
		iconv(furl,'gbk')  as furl
	   ,iconv(fip,'gbk') as fip
	   ,iconv(ftime,'gbk') as ftime
	from 
		kankan_odl.t_stat_url_upload
	where ds='${date}'
	cluster by fip
)a
INSERT OVERWRITE TABLE kankan_bdl.t_stat_url_upload_split PARTITION(ds='${date}')
REDUCE a.furl,a.fip,a.ftime
USING 't_stat_url_upload_split_mapper.py'
AS install,channel,peerid,version, package_name, installtype,fip,ftime 
```

方法2：

```shell
# kkpv_flow_flag.sh

use kankan_bdl;${UDFLIB};${UDF_CREATE};
add file ${comm_dir}/global_fun.py;
add file kkpv_flow_flag.py;
add file prov_ipbase.comb;
add file url_flag_v2.txt.2;
add file t_channel;
add archive ${arch_dir}/langconv.zip;
add archive ${arch_dir}/json.tar.gz;
add archive ${arch_dir}/yaml.tar.gz;
add archive ${arch_dir}/ua_parser.tar.gz;
set mapred.reduce.tasks=64;
from(
	select 
		from_unixtime(finsert_time,'H'),fu1,fu2,fu3,fu8,
		(case when(fu9 is NULL) then '' else fu9 end),
		fu12,fip,
        parse_url(uridecode(fu1),'HOST'),parse_url(uridecode(fu1),'PATH'),
        parse_url(uridecode(fu1),'QUERY'),
        parse_url(uridecode(fu9),'HOST'),parse_url(uridecode(fu9),'PATH'),
        parse_url(uridecode(fu9),'QUERY'),fu10,fu11,finsert_time
	from 
		kankan_odl.kkpv where ds='$date'
	cluster by fu2
)mapout
insert overwrite table kkpv_flow_flag partition(ds='$date')
reduce mapout.*
using 'python kkpv_flow_flag.py'
as
	hour string,
	url_query map<string,string>,
	prov int,
	city int,
	ref_search_engine string,
	add_id string,
	id_feature map<string,string>,
	uid string,
	contractNo string;
```

方法3：

```shell
# bl_fact_item_explore_android.sh

use xmp_data_mid;
add file bl_fact_item_explore_android.py;
insert overwrite table bl_fact_item_explore_android partition (ds='${date}',page='home',card)
select            	
	guid,phonetype,channelid,ip,sessionid,network,version
	,userid,movieid,model,sab,rsessionid,rn,refreshid,position,refreshnum,ts
    ,b.uid,b.uid_type,b.uid_video_type,b.duration
    ,a.retype
    ,'' as source
    ,a.card as card
 from
     (select transform(extdata_map,ts,attribute1) 
     	using 'python bl_fact_item_explore_android.py' 
     	as
            guid string,
            refreshnum string,
            ts bigint,
            card string,
            retype string
        from (
            select
                extdata_map
                ,ts
                ,attribute1
            from
                shoulei_bdl.bl_shoulei_event_fact
            where ds='${date}' and appid='45'
                and attribute1 in ('home_collect_content_show','home_dl_show')
                and extdata_map['contentlist'] is not null and type in ('video')
            union all
            select
                extdata_map
                ,ts
                ,'ad_show' as attribute1
            from
                shoulei_bdl.bl_ad_flow_shoulei_d
            where ds='${date}' and category='首页'
                and event_type='ad_show' and extdata_map['contentlist'] is not null 
                and platform='android'
            ) t
        ) a
        left join
        (select *
            ,'home_collect_content_show' as card
         from
            shoulei_mdl.short_media_info_merge
        ) b
        on a.movieid=b.video_id and a.card=b.card;
```

##### 写入到本地

```shell

```



#### shell

待补充

```shell

```

#### perl

待补充

```perl

```

#### c/c++

待补充

```c++

```

 ##参考

- 基础

  [Hadoop Streaming 编程(强烈推荐)](http://dongxicheng.org/mapreduce/hadoop-streaming-programming/)