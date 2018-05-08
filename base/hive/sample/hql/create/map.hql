-- map数据导入
use xmp_data_mid;
load data local inpath 'map.txt' into table map_test;

-- 数据查询
select b['b1'],get_json_object(c,'$.c1') from map_test;
select nvl(b['b1'],0),nvl(get_json_object(c,'$.c1'),0) from map_test;
