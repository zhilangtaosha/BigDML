-- 间隔统计
-- 中间插入的记录数
select
    id
    ,rn1
    ,rn1-rn2 as pos_diff
from
(
    select
        id
        ,rn1
        ,lag(rn1,1,0) over(order by rn1) as rn2
    from
    (
        select
            id
            ,rn1 
        from
        (
            select id
                ,s1
                ,row_number() over(order by cast(s1 as int)) as rn1
            from 
                xmp_data_mid.tbl_a
            where dtask='dur'
        )a
        where id='a1'
    )b
)c
where rn2!=0;

#查询结果
a1      3       1
a1      4       1
a1      7       3
a1      9       2
a1      10      1


-- s1差值
select
    id
    ,rn1
    ,rn1-rn2 as pos_diff
    ,s1
    ,s2
    ,s1-s2 as value_diff
from
(
    select
        id
        ,rn1
        ,lag(rn1,1,0) over(order by rn1) as rn2
        ,s1
        ,lag(s1,1,0) over(order by rn1) as s2
    from
    (
        select
            id
            ,s1
            ,rn1 
        from
        (
            select id
                ,s1
                ,row_number() over(order by cast(s1 as int)) as rn1
            from 
                xmp_data_mid.tbl_a
            where dtask='dur'
        )a
        where id='a1'
    )b
)c
where rn2!=0;

# 查询结果
a1      3       1       6       4       2.0
a1      4       1       8       6       2.0
a1      7       3       32      8       24.0
a1      9       2       67      32      35.0
a1      10      1       99      67      32.0


-- 在中间没有c1条件下的插入记录数(看看有没有优化的可能)
select
    c.id
   ,c.s1
   ,c.s1_pre
   ,c.s1-c.s1_pre
   ,c.rn1
   ,c.rn1_pre
   ,c.rn1-c.rn1_pre as pos_diff
from
(
    -- 原值选择
    select 
        id
        ,s1
        ,lag(s1,1,0) over(order by rn1) as s1_pre
        ,rn1
        ,lag(rn1,1,0) over(order by rn1) as rn1_pre
    from 
        xmp_data_mid.tbl_a_view
    where id='a1'
)c
left join
(
    select
        distinct a.rn1 as rn1
    from
    (
        -- 原值条件准备
        select 
            rn1
            ,lag(rn1,1,0) over(order by rn1) as rn1_pre
        from 
            xmp_data_mid.tbl_a_view
        where id='a1'
    )a
    full join
    (
        -- 过滤
        select 
            rn1
        from 
            xmp_data_mid.tbl_a_view
        where id='c1'
    )b
    where a.rn1_pre<b.rn1 and b.rn1<a.rn1
        and a.rn1_pre!=0  
)d
on c.rn1=d.rn1
where d.rn1 is null and c.rn1_pre!=0;
