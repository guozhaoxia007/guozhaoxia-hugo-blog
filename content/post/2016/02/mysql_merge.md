---
date: "2016-02-24T11:08:29+08:00"
title: "mysql分表"
categories:
    - mysql
    - merge
    - oneproxy

---
#### 需求
1. 提高插入查询速度
2. 便于归档

#### 数据容量估算
5k终端，单个终端1分钟4个点，假设1天运行12小时，5000终端1天将产生：4 * 60 * 12 * 5000 = 14400000条记录，一条记录82bytes 

**即一天产生：14400000 * 82 = 1180800000bytes = 1126.1 M = 1.1 G**
**即一月产生：4亿条记录，30G存储**

根据容量估算，除去查询效率不考虑外，单是存储问题就很严重，1w终端单月产生8亿60G，10w终端单月产生80亿600G。

#### 产品调研
1. oneproxy

  + 优点：
     + 对应用透明
     + 支持二级分表(tid, timestamp)
     + 多种分表方法(hash, range)
     + 使用简单方便
     + 性能测试，大大提高查询速度，插入速度也不会大的影响
     + 由于使用时间分表，极大方便归档
  
  + 缺点：
     + 需手动创建子表

2. mysql merge
  + 优点：
     + 对应用透明
     + 无需引入第三方软件
    
  + 缺点：
     + 子表需为MyISAM引擎
     + 无法使用表字段分表（即无法使用时间分表，只能人工分表）
     + 需手动创建子表
     + 一级分表
     + MERGE storage engine.  User-defined partitioning and the MERGE storage engine are not compatible.
     Tables using the MERGE storage engine cannot be partitioned. Partitioned tables cannot be merged.

#### 结论

