#!/bin/bash
cd `dirname $0`
KK_WORKSPACE=${KK_WORKSPACE:-"/usr/local/sandai/server"}
source $KK_WORKSPACE/bin/common/global_var.sh
comm_dir="${KK_WORKSPACE}/bin/common"
arch_dir="${KK_WORKSPACE}/archive"
echo ${comm_dir}

[ -z $date ]&&date=$1

# mysql查询数据并导出
sql="select 'in_id',fsubType,'0','0','0','0' from pgv_stat.t_channel "
${MYSQL10} -e "${sql}" > t_channel

sql="select 'out_id',url_id,contacterid,companyid,trim(out_ref_pattern),contractNo from pgv_stat.t_partner_v2 where flag=1"
${MYSQL10} -e "${sql}" >> t_channel

sql="select start,end,province_id,city_id,sp_id from pgv_stat_dimension.ipbase"
${MYSQL10} -e "${sql}" > prov_ipbase.comb

hql="
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
	select from_unixtime(finsert_time,'H'),fu1,fu2,fu3,fu8,
	(case when(fu9 is NULL) then '' else fu9 end),fu12,fip,
	parse_url(uridecode(fu1),'HOST'),parse_url(uridecode(fu1),'PATH'),
	parse_url(uridecode(fu1),'QUERY'),
	parse_url(uridecode(fu9),'HOST'),parse_url(uridecode(fu9),'PATH'),
	parse_url(uridecode(fu9),'QUERY'),fu10,fu11,finsert_time
	from kankan_odl.kkpv where ds='$date'
	cluster by fu2
	)mapout
	insert overwrite table kkpv_flow_flag partition(ds='$date')
	reduce mapout.*
	using 'python kkpv_flow_flag.py'
	as
	hour string,
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
	id_feature map<string,string>,
	url_id string,
	channel_base string,
	contacterid string,
	companyid string,
	search_engine string,
	uid string,
	is_vip string,
	url string,
	ref string,
	contractNo string"
echo "$hql"
${HIVE} -e "$hql"


ret=$?
if [ "$ret" != "0" ];then
	exit $ret
fi

exit 0
