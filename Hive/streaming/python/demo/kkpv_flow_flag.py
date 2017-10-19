#!/usr/bin/python

import sys,os
import re
reload(sys)
sys.setdefaultencoding('utf-8')

__author__ = "shallwe(zhangxiaowei@xunlei.com)"
import urllib,urlparse

os.environ['KK_WORKSPACE']="/usr/local/sandai/server/"
ENV_KK_WORKSPACE=os.environ['KK_WORKSPACE']
common_dir=ENV_KK_WORKSPACE+"bin/common"
conf_dir=ENV_KK_WORKSPACE+"conf"
arch_dir=ENV_KK_WORKSPACE+"archive"

sys.path.append(common_dir)
sys.path.append(arch_dir+'/langconv.zip')
sys.path.append('.')
sys.path.append('langconv.zip')
sys.path.append('json.tar.gz')
sys.path.append('yaml.tar.gz')
sys.path.append('ua_parser.tar.gz')
import global_fun
print>>sys.stderr, sys.path

ipbase = []
ipsect = []

def load_ipbase(ipbase_path):
	global ipbase
	for line in open(ipbase_path):
		start,end,prov,city,sp = line.rstrip().split("\t")
		ipbase.append([int(start),int(end),prov,city,sp])
		ipsect.append(int(start))

str_conf = {}

def load_url_flag(filename):
	global str_conf

	#column_patch:0,1:page,2domain,3:url
	for line in open(filename):
		(column,column_flag,column_patch,reg) = line.rstrip().split("\t")
		str_conf.setdefault(column,{}).setdefault(column_flag,"%s\t%s" % (column_patch,"^"+reg+"$"))
in_channels = {}
out_channels = {}

def load_channel(filename):
	global in_channels
	global out_channels
	for line in open(filename):
		(channel_flag,channelid,contacterid,companyid,refreg,contractNo) = line.rstrip().split("\t")
		if(channel_flag == "in_id"):
			in_channels[channelid] = [contacterid,companyid,refreg,contractNo]
		else:
			out_channels[channelid] = [contacterid,companyid,refreg,contractNo]
#		ichannels[channelid] = [channel_flag,contacterid,companyid]

def parse_url_flag_once(url,domain,flag_type):
	if flag_type not in str_conf:
		return "0";
	cur_flag_dict = str_conf[flag_type]
	for flag in cur_flag_dict:
		column_patch,reg = cur_flag_dict[flag].split("\t")
	#	print column_patch,reg
		if column_patch == "1":
			if re.match(reg,url) is not None:
				return flag
		if column_patch == "2":
			if re.match(reg,domain) is not None:
				return flag;
	return "0"

def parse_url_remove(url,url_domain,ref,ref_domain):
	ret = parse_url_flag_once(url,url_domain,"remove")
	if ret == "0" :
		return False
	else:
		return True

def parse_url_flag(url,domain,flags):

	ret = []
	for flag_type in flags:
		ret.append(parse_url_flag_once(url,domain,flag_type))
	return ret

def parse_url_id_once(url,reg):
	regex_ret = re.findall(reg,url)
	if len(regex_ret) != 0:
		return regex_ret[0]
	return "0"

def display_for_map(a):
	if a:
		return ','.join([x[0]+":"+str(x[1]) for x in a.items()])
	else:
		return '0:0'

def parse_url_id(url):
	cur_flag_dict = str_conf["ids"]
#	ret = []
	ret = {}
	for id in cur_flag_dict:
		column_patch,reg = cur_flag_dict[id].split("\t")
	#	print column_patch,reg
#		ret.append(parse_url_id_once(url,reg))
		ret.setdefault(id,parse_url_id_once(url,reg))
	ret_str = display_for_map(ret)
	return [ret_str]

def checkvalue(value):
	if(value is not None):
		return value
	else:
		return '0'

def user_agent(user_agent_str):
	from ua_parser import user_agent_parser
	ua_ret = user_agent_parser.Parse(user_agent_str);
	device = checkvalue(ua_ret['device']['family'])
	os_major = checkvalue(ua_ret['os']['major'])
	os_minor = checkvalue(ua_ret['os']['minor'])
	os_patch = checkvalue(ua_ret['os']['patch'])
#	device = ua_ret['device']['family'] if  ua_ret['device']['family'] is not None else '0'
#	os_major = ua_ret['os']['major'] if ua_ret['os']['major'] is not None else '0'
#	os_minor = ua_ret['os']['minor'] if ua_ret['os']['minor'] is not None else '0'
#	os_patch = ua_ret['os']['patch'] if ua_ret['os']['patch'] is not None else '0'
	os_version = "%s.%s.%s" % (os_major,os_minor,os_patch)
	agent_major = checkvalue(ua_ret['user_agent']['major'])
	agent_minor = checkvalue(ua_ret['user_agent']['minor'])
	agent_patch = checkvalue(ua_ret['user_agent']['patch'])
#	agent_major = ua_ret['user_agent']['major'] if ua_ret['user_agent']['major'] is not None else '0'
#	agent_minor = ua_ret['user_agent']['minor'] if ua_ret['user_agent']['minor'] is not None else '0'
#	agent_patch = ua_ret['user_agent']['patch'] if ua_ret['user_agent']['patch'] is not None else '0'
	agent_version = "%s.%s.%s" % (agent_major,agent_minor,agent_patch)

	return (device,ua_ret['os']['family'],os_version,ua_ret['user_agent']['family'],agent_version)
#	return ('0','0','0','0','0')

def parse_url(url):
	pr =  urlparse.urlparse(url)
#	query_arr = [item.split('=') for item in pr.query.split("&")]
#	query_dict = {}
#	for item in query_arr:
#		if len(item) == 2:
#			query_dict.setdefault(item[0],item[1])
#	query_dict_str = ",".join([x[0]+":"+str(x[1]) for x in query_dict.items()])
#	if pr.path != "/":
#		path = pr.path
#	else:
#		path = ""

#	path = pr.path if pr.path != "/" else ""

#	return (pr.netloc,pr.netloc+path,query_dict_str)
	return ('','','')

def parse_url(url_net,url_path,url_querys):
	query_arr = [item.split('=') for item in url_querys.split("&")]
	query_dict = {}
	id = ""
	for item in query_arr:
		if len(item) == 2:
			if(item[0]=="id"):
				id = item[1]
			query_dict.setdefault(item[0],item[1])
	query_dict_str = ",".join([x[0]+":"+str(x[1]) for x in query_dict.items()])
	if url_path != "/":
		path = url_path
	else:
		path = ""
	return (url_net,url_net+path,query_dict_str,id)

def parse_ip(ipstr):
	from bisect import bisect
	ip = 0
	try:
		ip = global_fun.ipstr2unit(ipstr)
	except:
		return ["0","0","0"]
	sect_number = bisect(ipsect,ip) -1
	if sect_number >=0 and sect_number < len(ipbase):
		item = ipbase[sect_number]
		if (int(ip)<=item[1]):
			return [item[2],item[3],item[4]]
	return ["0","0","0"]

def parse_channel(url_id,ref):
	entrance = 0
	[channel_type,contactid,companyid,search_engine,contractNo] = ['0','0','0','0','0']
	if(ref==""):
		entrance = 1
	elif(ref!='' and (re.match(".*kankan.com.*",ref) == None)):
		entrance = 1

	cur_flag_dict = str_conf["add_id"]
	for id in cur_flag_dict:
		column_patch,reg = cur_flag_dict[id].split("\t")
		if(re.match(reg,ref)):
			if(url_id==""):
				url_id = id
	cur_flag_dict = str_conf["search_engine"]

	for id in cur_flag_dict:
		column_patch,reg = cur_flag_dict[id].split("\t")
		if(re.match(reg,ref)):
			search_engine = id

	if(url_id=="731009" and re.match('.*hao123.com.*',ref) and re.match('.*vfm=bdvppzq.*',ref)==None and re.match('.*frp=bdbrand.*',ref)==None):
               	 url_id = "731028"
        if(url_id=="731018" and re.match('.*v.hao.qq.com.*',ref)):
                url_id = "731089"
	if(url_id=="" and re.match('.*www.haosou.com.*',ref)):
		url_id="751034"

	if(in_channels.has_key(url_id)):
		channel_type = "in_id"
	elif(out_channels.has_key(url_id)):
		channel_type = "out_id"
		[contactid,companyid,refreg,contractNo] = out_channels[url_id]
		if(re.match(refreg,ref) or ref==""):
			url_id = url_id
		else:
			url_id = "0"

	elif(ref.replace(" ","") == ""):
		channel_type = "direct"
	elif(search_engine!="0"):
		channel_type = "seo"
	elif(entrance == 1):
		channel_type = "out_other"

	return  [url_id,channel_type,contactid,companyid,search_engine,contractNo]



#main process
load_ipbase("prov_ipbase.comb")#ipbase
load_url_flag("url_flag_v2.txt.2")#str_conf
load_channel("t_channel")
regex=re.compile('.*search.xmp.kankan.com*')

for line in sys.stdin:
	try:
		(hour,url,cookieid,peerid,useragent,ref,session_id,ip,url_net,url_path,url_querys,ref_net,ref_path,ref_querys,uid,is_vip,finsert_time) = line.rstrip().split("\t")
		url = urllib.unquote_plus(url)
		useragent = urllib.unquote_plus(useragent)
		ref = urllib.unquote_plus(ref)
		if not (global_fun.is_cookieid_eff(cookieid)):
			continue

		(url_domain,pure_url,url_query,url_id) = parse_url(url_net,url_path,url_querys)
		(ref_domain,pure_ref,ref_query,ref_id) = parse_url(ref_net,ref_path,ref_querys)

		if parse_url_remove(pure_url,url_domain,pure_ref,ref_domain) == True:
			continue
		[url_id,channel_type,contacterid,companyid,search_engine,contractNo] = parse_channel(url_id,ref)
		channel_feature = [url_id,channel_type,contacterid,companyid,search_engine]

		meta_feature = [hour,cookieid,peerid,session_id,ip,finsert_time]
		url_ref_feature = [url_domain,pure_url,url_query,ref_domain,pure_ref,ref_query]

		[device,os,os_version,ua,ua_version] = user_agent(useragent)
		ua_feature = [device,os,os_version,ua,ua_version]

		flags = ["url_flag"]
		url_flags = parse_url_flag(pure_url,url_domain,flags)

		flags = ["url_flag","search_engine","add_id"]
		ref_flags = parse_url_flag(pure_ref,ref_domain,flags)

		id_feature = parse_url_id(pure_url)
		ip_feature = parse_ip(ip)

        m1=re.match(regex,pure_ref)
		if m1 is None:
			continue

		pv_feature = []
		pv_feature.extend(meta_feature)
		pv_feature.extend(url_ref_feature);
		pv_feature.extend(ua_feature)
		pv_feature.extend(ip_feature)
		pv_feature.extend(url_flags)
		pv_feature.extend(ref_flags)
		pv_feature.extend(id_feature)
		pv_feature.extend(channel_feature)
		pv_feature.extend([uid,is_vip])
		pv_feature.extend([url,ref])
		pv_feature.extend([contractNo])
		print "\001".join(pv_feature)
	except:
		#print >> sys.stderr,line
		continue
