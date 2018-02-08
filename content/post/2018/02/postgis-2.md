---
date: "2018-02-07T15:07:13+08:00"
title: "postgis-2"

---
## 0. 创建空间字段准备
```
CREATE EXTENSION postgis;
```
```
-- Geometry
-- Method 1
SELECT AddGeometryColumn ('scheme'，'cities', 'the_geom', 4326, 'POINT', 2);

AddGeometryColumn(
  <schema_name>,
  <table_name>,
  <column_name>,
  <srid>,
  <type>,
  <dimension>
)

-- Method 2
CREATE TABLE ROADS ( ID int4, ROAD_NAME varchar(25), geom geometry(LINESTRING,4326) );

CREATE TABLE global_points (
    id SERIAL PRIMARY KEY,
    name VARCHAR(64),
    location GEOGRAPHY(POINT,4326)
  );

-- Method 3
ALTER TABLE roads ADD COLUMN geom2 geometry(LINESTRINGZ,4326);
```
```
-- geography
CREATE TABLE testgeog(gid serial PRIMARY KEY, the_geog geography(POINT,4326) );
CREATE TABLE testgeog(gid serial PRIMARY KEY, the_geog geography(POINTZ,4326) );


```
## 1. 插入数据
```
-- Method 1: ST_GeomFromText??
INSERT INTO roads (road_id, roads_geom, road_name) VALUES (3,ST_GeomFromText('LINESTRING(192783 228138,192612 229814)',-1),'Paul St');
-- ??
SELECT ST_GeomFromText('LINESTRING(-71.160281 42.258729,-71.160837 42.259113,-71.161144 42.25932)',4326);

-- Method 2: WKT
INSERT INTO table ( SHAPE, NAME )VALUES ( GeomFromEWKT('SRID=4326;POINTM(116.39 39.9 10)'), '北京' );

```

## 2. 读取数据
```
SELECT id, ST_AsText(the_geom), ST_AsGeoJson(the_geom), ST_AsEwkt(the_geom), ST_X(the_geom), ST_Y(the_geom) FROM cities;


```
## 3. 知识点
### 3.0. WKT & WKB
the Well-Known Text (WKT) form and the Well-Known Binary (WKB) form.

Examples of the text representations (WKT) of the spatial objects of the features are as follows:

```
POINT(0 0)

LINESTRING(0 0,1 1,1 2)

POLYGON((0 0,4 0,4 4,0 4,0 0),(1 1, 2 1, 2 2, 1 2,1 1))

MULTIPOINT((0 0),(1 2))

MULTILINESTRING((0 0,1 1,1 2),(2 3,3 2,5 4))

MULTIPOLYGON(((0 0,4 0,4 4,0 4,0 0),(1 1,2 1,2 2,1 2,1 1)), ((-1 -1,-1 -2,-2 -2,-2 -1,-1 -1)))

GEOMETRYCOLLECTION(POINT(2 3),LINESTRING(2 3,3 4))
```
```
bytea WKB = ST_AsBinary(geometry);
text WKT = ST_AsText(geometry);
geometry = ST_GeomFromWKB(bytea WKB, SRID);
geometry = ST_GeometryFromText(text WKT, SRID);
```
```
INSERT INTO geotable ( the_geom, the_name )
  VALUES ( ST_GeomFromText('POINT(-126.4 45.32)', 312), 'A Place');
```
### 3.1. Geometry
### 3.2. geography
>
The new GEOGRAPHY type allows you to store data in longitude/latitude coordinates, but at a cost: there are fewer functions defined on GEOGRAPHY than there are on GEOMETRY; those functions that are defined take more CPU time to execute.
>