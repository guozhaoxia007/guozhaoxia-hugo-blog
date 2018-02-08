---
date: "2016-02-20T23:18:34+08:00"
title: "pytz"
categories:
    - python
    - timezone
    - pytz
---
# pytz使用

## 使用场景
- 查询，如果前端输入start_time, end_time，后台计算月报（每天开始结束时间）和年报（每月开始结束时间）
- 定时任务，统计前一天的数据，即知道年月日，后台计算start_time, end_time

## 实验1，夏令时和冬令时
```
# 美东、中国标准、印度标准、印尼西部
['UTC', 'US/Eastern', 'Asia/Shanghai', 'Asia/Kolkata', 'Asia/Jakarta']
fmt = '%Y-%m-%d %H:%M:%S %Z%z'

for tz in timezones:
    p_tz = timezone(tz)
    loc_dt = p_tz.localize(datetime(2015,4,1,8,0,0))
    print loc_dt.strftime(fmt)

2015-04-01 08:00:00 EDT-0400
2015-04-01 08:00:00 CST+0800
2015-04-01 08:00:00 IST+0530
2015-04-01 08:00:00 WIB+0700


for tz in timezones:
    p_tz = timezone(tz)
    loc_dt = p_tz.localize(datetime(2015,12,1,8,0,0))
    print loc_dt.strftime(fmt)

2015-12-01 08:00:00 EST-0500
2015-12-01 08:00:00 CST+0800
2015-12-01 08:00:00 IST+0530
2015-12-01 08:00:00 WIB+0700
```
## 实验2
```
In [146]: now = int(time.time())

In [147]: now
Out[147]: 1451015286

In [148]: utc_dt = utc.localize(datetime.utcfromtimestamp(now))

In [149]: utc_dt.strftime(fmt)
Out[149]: '2015-12-25 03:48:06 UTC+0000'

In [151]: for tz in timezones:
    p_tz = timezone(tz)
    p_dt = p_tz.normalize(utc_dt.astimezone(p_tz))
    print p_dt.strftime(fmt)
   .....:
2015-12-24 22:48:06 EST-0500
2015-12-25 11:48:06 CST+0800
2015-12-25 09:18:06 IST+0530
2015-12-25 10:48:06 WIB+0700
```

mktime:（使用美东时区的datetime）
在东8区执行：
```
int(time.mktime(time.strptime('2015-12-24 22:48:06', '%Y-%m-%d %H:%M:%S'))

1450968486
```
在美东时区执行
```
int(time.mktime(time.strptime('2015-12-24 22:48:06', '%Y-%m-%d %H:%M:%S'))
1451015286
```

## timestamp -> datetime
```
def timestamp2datetime(timestamp, tzinfo, fmt="%Y-%m-%d %H:%M:%S %Z%z"):
    utc = pytz.utc
    utc_dt = utc.localize(datetime.utcfromtimestamp(timestamp))
    tz = timezone(tzinfo)
    dt = tz.normalize(utc_dt.astimezone(tz))
    return dt, dt.strftime(fmt)
    
In [178]: timestamp2datetime(1451015286, 'Asia/Shanghai')
Out[178]: '2015-12-25 11:48:06 CST+0800'

In [179]: timestamp2datetime(1451015286, 'US/Eastern')
Out[179]: '2015-12-24 22:48:06 EST-0500'

```
 
 美国2015.3.8 02:00（当地时间）进入夏令时：
 
```
In [181]: timestamp2datetime(1425794400, 'US/Eastern')
Out[181]: '2015-03-08 01:00:00 EST-0500'
In [204]: timestamp2datetime(1425794400, 'Asia/Shanghai')
Out[204]: '2015-03-08 14:00:00 CST+0800'

In [184]: timestamp2datetime(1425797999, 'US/Eastern')
Out[184]: '2015-03-08 01:59:59 EST-0500'
In [207]: timestamp2datetime(1425797999, 'Asia/Shanghai')
Out[207]: '2015-03-08 14:59:59 CST+0800'

In [180]: timestamp2datetime(1425798000, 'US/Eastern')
Out[180]: '2015-03-08 03:00:00 EDT-0400'  # 注：2点变3点
In [208]: timestamp2datetime(1425798000, 'Asia/Shanghai')
Out[208]: '2015-03-08 15:00:00 CST+0800'
```

美国2015.11.1 02:00（当地时间）进入夏令时：
```
In [202]: timestamp2datetime(1446357599, 'US/Eastern')
Out[202]: '2015-11-01 01:59:59 EDT-0400'
In [209]: timestamp2datetime(1446357599, 'Asia/Shanghai')
Out[209]: '2015-11-01 13:59:59 CST+0800'

In [203]: timestamp2datetime(1446357600, 'US/Eastern')
Out[203]: '2015-11-01 01:00:00 EST-0500' //注：2点变1点
In [210]: timestamp2datetime(1446357600, 'Asia/Shanghai')
Out[210]: '2015-11-01 14:00:00 CST+0800'
```
## datetime -> timestamp
```
def datetime2timestamp(dt):
    utc_tz = timezone("UTC")
    utc_dt = utc_tz.normalize(dt.astimezone(utc_tz))
    return calendar.timegm(utc_dt.timetuple())


def datetime_to_unixtime(year, month, day, hour=0, minute=0, second=0, tzinfo="Asia/Shanghai"):
    """
    >>> datetime_to_unixtime(2015, 11, 1, hour=1, tzinfo='US/Eastern')
    1446357600
    """
    tz = timezone(tzinfo)
    dt = datetime(year, month, day, hour, minute, second)
    dt = tz.localize(dt)
    utc_tz = timezone("UTC")
    utc_dt = utc_tz.normalize(dt.astimezone(utc_tz))

    return calendar.timegm(utc_dt.timetuple())
```

## 总结
datetime + tzinfo是关键
epochtime转datetime，datetime带tzinfo才知道转给哪个时区的人看
datetime转epochtime，datetime带tzinfo才知道用哪个时区转成UTC时间
