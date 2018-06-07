#!/bin/perl
# substr(fu1,2,5),fu2,fu5,fu7,fip,finsert_time
# 2A5F8   [3,0,8] ["5486","0","0"]        0,1,0   124.91.9.111    1517673596
while read line;do
    infos=($line)
    echo -e -n "hahh:${infos[0]}\t${infos[1]}\t${infos[2]}\t${infos[3]}\t${infos[4]}"
    ds=`date -d @${infos[5]} "+%Y-%m-%d"`
    echo -e -n "${ds}\n"
done <test.data


exit 0
