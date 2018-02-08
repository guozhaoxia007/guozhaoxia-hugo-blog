---
date: "2018-02-07T15:07:13+08:00"
title: "postgis"

---
# Chapter 4. Using PostGIS: Data Management and Queries
http://postgis.net/docs/manual-2.3/using_postgis_dbmanagement.html

## 4.1. GIS Objects
### 4.1.1. OpenGIS WKB and WKT
OpenGIS定义了两种空间表达对象：the Well-Known Text(WKT) form和the Well-Known Binary(WKB) form. WKT和WKB都包含了对象的类型和坐标。

WKT举例：

>POINT(0 0)
>
>LINESTRING(0 0,1 1,1 2)
>
>POLYGON((0 0,4 0,4 4,0 4,0 0),(1 1, 2 1, 2 2, 1 2,1 1))
>
>MULTIPOINT((0 0),(1 2))
>
>MULTILINESTRING((0 0,1 1,1 2),(2 3,3 2,5 4))
>
>MULTIPOLYGON(((0 0,4 0,4 4,0 4,0 0),(1 1,2 1,2 2,1 2,1 1)), ((-1 -1,-1 -2,-2 -2,-2 -1,-1 -1)))
>
>GEOMETRYCOLLECTION(POINT(2 3),LINESTRING(2 3,3 4))
>
OpenGIS要求在存储空间对象时要包含a spatial referencing system identifier(SRID).

各种转换接口：

```
bytea WKB = ST_AsBinary(geometry);
text WKT = ST_AsText(geometry);
geometry = ST_GeomFromWKB(bytea WKB, SRID);
geometry = ST_GeometryFromText(text WKT, SRID);
```

插入语句举例：

```
INSERT INTO geotable ( the_geom, the_name )
  VALUES ( ST_GeomFromText('POINT(-126.4 45.32)', 312), 'A Place');
```
### 4.1.2. PostGIS EWKB, EWKT and Canonical Forms
OGC格式只支持2D

PostGIS扩展出了一个OBC的超集（每个合法的WKB/WKT也是合法的EWKB/EWKT），可能未来会不同，尤其OGC新出一个有冲突的新格式，所以不要依赖这个功能。

PostGIS EWKB/EWKT增加了3dm, 3dz, 4d坐标

EWKT举例：

>
>POINT(0 0 0) -- XYZ

>SRID=32632;POINT(0 0) -- XY with SRID

>POINTM(0 0 0) -- XYM

>POINT(0 0 0 0) -- XYZM

>SRID=4326;MULTIPOINTM(0 0 0,1 2 1) -- XYM with SRID

>MULTILINESTRING((0 0 0,1 1 0,1 2 1),(2 3 1,3 2 1,5 4 1))

>POLYGON((0 0 0,4 0 0,4 4 0,0 4 0,0 0 0),(1 1 0,2 1 0,2 2 0,1 2 0,1 1 0))

>MULTIPOLYGON(((0 0 0,4 0 0,4 4 0,0 4 0,0 0 0),(1 1 0,2 1 0,2 2 0,1 2 0,1 1 0)),((-1 -1 0,-1 -2 0,-2 -2 0,-2 -1 0,-1 -1 0)))

>GEOMETRYCOLLECTIONM( POINTM(2 3 9), LINESTRINGM(2 3 4, 3 4 5) )

>MULTICURVE( (0 0, 5 5), CIRCULARSTRING(4 0, 4 4, 8 4) )

>POLYHEDRALSURFACE( ((0 0 0, 0 0 1, 0 1 1, 0 1 0, 0 0 0)), ((0 0 0, 0 1 0, 1 1 0, 1 0 0, 0 0 0)), ((0 0 0, 1 0 0, 1 0 1, 0 0 1, 0 0 0)), ((1 1 0, 1 1 1, 1 0 1, 1 0 0, 1 1 0)), ((0 1 0, 0 1 1, 1 1 1, 1 1 0, 0 1 0)), ((0 0 1, 1 0 1, 1 1 1, 0 1 1, 0 0 1)) )

>TRIANGLE ((0 0, 0 9, 9 0, 0 0))

>TIN( ((0 0 0, 0 0 1, 0 1 0, 0 0 0)), ((0 0 0, 0 1 0, 1 1 0, 0 0 0)) )
>

各种转换接口：

```
bytea EWKB = ST_AsEWKB(geometry);
text EWKT = ST_AsEWKT(geometry);
geometry = ST_GeomFromEWKB(bytea EWKB);
geometry = ST_GeomFromEWKT(text EWKT);
```

插入语句举例：

```
INSERT INTO geotable ( the_geom, the_name )
  VALUES ( ST_GeomFromEWKT('SRID=312;POINTM(-126.4 45.32 15)'), 'A Place' )
```

### 4.1.3. SQL-MM Part 3

## 4.2. PostGIS Geography Type
Geography类型支持geographic坐标，也叫geodetic坐标，或lat/lon或lon/lat

PostGIS geometry类型的基础是plane平面。在平面上两个点之间最短的路径是一条直线。即，areas, distances, lengths, intersections等计算都可以用笛卡尔数学和直线向量计算。

PostGIS geographic类型的基础是一个球体。球面上两点之间最短的路径是一个大圆弧。那意味着计算球体上的面积，距离，长度，交点等会用到更复杂的计算方法。

因为计算比较复杂，所以在geography类型上比geometry类型的函数更少。

有一个限制是它只支持WBS84经纬度(SRID: 4326)。它用了一种新的叫geography的数据类型。GEOS函数都不支持这种类型。作为一种替代方法可以来回转换geometry和geography.

### 4.2.1. Geography Basics
Geography类型只支持最简单的功能。标准的geometry类型数据会自动转换成geography如果SRID是4326.也可以用EWKT和EWKB插入数据。
- POINT: 用geometry 2d点创建表：
```
CREATE TABLE testgeog(gid serial PRIMARY KEY, the_geog geography(POINT, 4326));
```
加上z坐标创建表：
```
CRETAE TABLE testgeog(gid serial PRIMARY KEY, the_geog geography(POINTZ, 4326));
```
- LINESTRING
- POLYGON
- MULTIPOINT
- MULTILINESTRING
- MULTIPOLYGON
- GEOMETRYCOLLECTION
新的geography字段没有注册到geometry_columns里。他们被注册到一个新的叫geography_columns的视图里。
添加geography列的时候，不像geometry，不用单独运行AddGeometryColumns()
```
CREATE TABLE global_points(
    id SERIAL PRIMARY KEY,
    name VARCHAR(64),
    location GEOGRAPHY(POINT, 4326)
);
```
注意，location列有GEOGRAPHY类型，这种类型支持两个可选的变量：一个是形状和大小；一个是SRID限制坐标参考系。

允许的类型值包括：POINT, LINESTRING, POLYGON, MULTIPOINT, MULTILINESTRING, MULTIPOLYGON.也包括后缀为Z, M和ZM的类型。比如，LINESTRINGM只允许有三个维度，而POINTZM要有4个维度。

SRID变量现在限制只能用4326(WGS84)。如果没指定SRID，会使用值为0（未定义的球体），所有的计算还是用WGS84.

在将来，SRID会允许除了WGS84以外的值。

一旦你创建了表，你可以在GEOGRAPHY_COLUMNS表里看到它：
```
SELECT * FROM geography_columns;
```
插入数据：
```
INSERT INTO global_points(name, location) VALUES('Town', ST_GeographyFromText('SRID=4326; POINT(-110 30)'));
```
创建索引。
```
CREATE INDEX global_points_gix ON global_points USING GIST(location);
```
查询和度量函数的单位是米，（或平方米）
```
SELECT name FROM global_points WHERE ST_DWITHIN(location, ST_GeographyFromText('SRID=4326; POINT(-110, 29)'), 1000000);
```
你可以看到GEOGRAPHY的力量，通过计算一个飞机从seattle到london(LINESTRING(-122.33 47.606, 0.0 51.5)),来到Reykjavik(POINT(-21.96 64.15)).
```
-- Distance calculation using GEOGRAPHY (122.2km)
SELECT ST_Distance('LINESTRING(-122.33 47.606, 0.0 51.5)'::geography, 'POINT(-21.96 64.15)'::geography);

-- Distance calculation using GEOMETRY (13.3 "degrees")
 SELECT ST_Distance('LINESTRING(-122.33 47.606, 0.0 51.5)'::geometry, 'POINT(-21.96 64.15)':: geometry);
```
GEOGRPHY类型计算了真实的球体上的最短距离。
GEOMETRY类型计算了一个无意义的笛卡尔距离（平面地图的直线路径）。计算的结果单位名义上是degrees,但是结果却与两点之间真实的角差不相符，所以叫他们degrees是错误的。
### 4.2.2. When to use Geography Data type over Geometry data type
GEOGRAPHY类型允许存入longitude/latitude坐标点数据，但是有一个代价：GEOGRAPHY支持的函数比较少，而且这些函数执行时会消耗更多的CPU。
根据你的应用场景来选择类型。你的数据会跨越全球还是大的大陆区域，或者是州、县或市的地方？

- 如果数据范围在一个小范围内，你可以使用GEOMETRY而不用担心投影的问题，性能和功能都是最佳体验。

- 如果数据范围是全球或大片大陆区域，你会发现使用GEOGRAPHY比较好。位置数据可以使用longitude/latitude.

- 如果你不懂投影，也不想了解他们，而且GEOGRAPHY有限的函数也可以接受，那么GEOGRAPHY比GEOMETRY要更简单。

[Geography vs. Geometry](http://postgis.net/docs/manual-2.3/PostGIS_Special_Functions_Index.html#PostGIS_TypeFunctionMatrix)
### 4.2.3. Geography Advanced FAQ
#### 4.2.3.1. Do you calculate on the sphere or the spheroid?
默认情况下，所有的距离和面积计算是在球体上完成的。你可以发现在本地地方区域的计算结果与平面计算结果是基本对应的。更大的区域的话，球面计算结果要比平面计算结果精确多了。

所有的geography函数都有一个可选项是球面计算，通过设置布尔参数为FALSE，这或许会提高计算的速度，部分场景下geometries是非常简单的。
#### 4.2.3.2. What about the data-line and the poles?
所有的计算都不涉及[日界线和极点]()的概念。球形形状，越过日界线，从计算的观点来看，与任何其他的形状没有什么不同。
## 4.3. Using OpenGIS Standards
### 4.3.1. The SPATIAL_REF_SYS Table and Spatial Reference Systems
### 4.3.2. The GEOMETRY_COLUMNS VIEW
### 4.3.3. Creating a Spatial Table
### 4.3.4. Manually Registering Geometry Columns in geometry_columns
### 4.3.5. Ensuring OpenGIS compliancy of geometries
### 4.3.6. Dimensionally Extended 9 Intersection Model (DE-9IM)
## 4.4. Loading GIS (Vector) Data
### 4.4.1. Loading Data Using SQL
### 4.4.2. shp2pgsql: Using the ESRI Shapefile Loader
## 4.5. Retrieving GIS Data
### 4.5.1. Using SQL to Retrieve Data
### 4.5.2. Using the Dumper
## 4.6. Building Indexes
### 4.6.1. GiST Indexes
### 4.6.2. BRIN Indexes
### 4.6.3. Using Indexes
## 4.7. Complex Queries
### 4.7.1. Taking Advantage of Indexes
### 4.7.2. Examples of Spatial SQL

