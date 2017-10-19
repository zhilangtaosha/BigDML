use kankan_bdl;
create external table if not exists kkpv_flow_flag
(hour string,
cookieid string,
peerid string,
session_id string,
ip string,
finsert_time string,
url_domain string,
pure_url string,
url_query map<string,string>,
ref_domain string,
pure_ref string,
ref_query map<string,string>,
device string,
os string,
os_version string,
ua string,
ua_version string,
prov int,
city int,
isp int,
url_flag string,
ref_flag string,
ref_search_engine string,
add_id string,
id_feature map<string,string>
) 
partitioned by(ds string) 
row format delimited fields terminated by '\001';

create external table if not exists kkpv_flow_flag_session (
session_id string,
start_ds bigint,
end_ds bigint,
pv int,
duration int,
simplepath array<string>,
last_step string )
partitioned by (ds string)
row format delimited fields terminated by '\001';
