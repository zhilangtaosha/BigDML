-- 详情页推荐位曝光分割
add file pos_split.py;
select
    transform(ds,xl_urldecode(extdata_map['movielist']))
    using 'python pos_split.py'
    as (ds,pos,movieid)
from
    shoulei_bdl.bl_shoulei_event_fact
where ds='20180425' and appid='45' and type='video'
    and eventname='android_videodetail' and attribute1='videoDetail_recommend_show'
    and extdata_map['movielist'] is not null
limit 10;
