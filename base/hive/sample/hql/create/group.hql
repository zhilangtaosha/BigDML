select ds,
	nvl(srctbl,'total'),
	nvl(srcdb,'total'),
	sum(datasize)
from 
	xmp_data_mid.group_test
group by ds,srctbl,srcdb
grouping sets ((ds),(ds,srctbl),(ds,srcdb));
