##HiveUDF编写指南
[TOC]

### 基础

#### jar包引入方式

在开发了hive的udf udaf udtf函数的jar文件后，需要将jar文件放入hive环境中才可以使用,可通过以下三种方法加入：

- 使用add jar path/test.jar;方法加入

该方法的缺点是每次启动Hive的时候都要从新加入，退出hive就会失效。

- 通过设置hive的配置文件hive-site.xml 加入，在配置文件中增加配置,保存即可。

```xml
<property>
<name>hive.aux.jars.path</name>
<value>file:///jarpath/all_new1.jar,file:///jarpath/all_new2.jar</value>
</property>
```

该方法比第一种方法方便很多。不需要每次启动Hive执行命令加入，只是配置稍微复杂一些。

- 在${HIVE_HOME}中创建文件夹auxlib  ，然后将自定义jar文件放入该文件夹中。

个人推荐这种方法，方便快捷。

#### 编写jar包

hive udf的编写需要引入的jar包（参见lib目录下）：

- hive-exec-xxx.jar 
- hadoop-core-xxx.jar

==关键点==：

继承udf基类

idea工具的使用

 ##参考