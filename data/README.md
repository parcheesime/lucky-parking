## Todo

Problem: There is no development database. Right now we have to make all changes in production. 

The database consists of the lacity data set but also some external sources. We'd like to document those sources and be able to reproduce the database locally for development, staging, etc. 

Additionally, we'd like the data in the database to be updated programmatically. 

- Figure out where each table in production database comes from
    - Download / view data from lacity, find the table that corresponds with
    - Start a new PostGIS database and see which ones are default tables
- Figure out which data and tables are actually used by the application
- Read Greg's `upload.py` file and use or modify as necessary to make a local version

9 Tables

- `citations` - per Greg, attempt to take lacity data and compress it without losing info
- `neighborhood_councils` - empty
- `spatial_ref_sys` - postgis default
- `test1` - lacity data + geometries column
- `us_gaz` - (guess) postgis default - state names and abbreviations
- `us_lex` - (guess) postgis default
- `us_rules` - (guess) postgis default
- `zip_4326` - zip, geo_4326 columns, only one row
- `zipcodes` - zip code, shape, the_geom
    - geojson - multipolygon representing zip code border
    - 311 rows total, doesn't actually include all 515 zip codes in LA

Which tables are used

- only `test1`, `zipcodes` and PostGIS function (which maybe use other tables?)
- questions
    - how did geometries get appended the parking citation data?
        - geometries can be self generated, it is of the form
        {
            type: "Point",
            coordinates: [<latitude_column_value>, <longitude_column_value>]
        }
        - in [`citation-analysis branch`](https://github.com/hackforla/lucky-parking/tree/citation-analysis/src/data)
            - `make_dataset.py` appears to download the csv and cleans it, reformatting lat/lon
            - `upload.py` reads from a geojson file and converts it to postgis database
            - some logic and files referring to sampling

    - where did zip codes come from?
        - still need to investigate

Left to do
- ~~Figure out where zip codes came from~~
- see if we can run `citation-analysis` scripts
    - if they work, move them into this directory/branch and document how to use them
    - if they don't, fix them or ask greg to



**Zip Codes Table**
- [Source](https://data.lacounty.gov/Geospatial/ZIP-Codes/65v5-jw9f)
    - Source has the following columns: ObjectID, ZipCode, Shape_area, Shape_len
    - Our table has an additional column, the_geom


**Setting up Local DB Environment (Ubuntu)**
1. Follow this guide from StackOverflow to initially setup the database
    - https://stackoverflow.com/questions/53267642/create-new-local-server-in-pgadmin
2. Install PostGis ([more info](https://trac.osgeo.org/postgis/wiki/UsersWikiPostGIS24UbuntuPGSQL10Apt))
```
sudo apt install postgresql-12-postgis-3
sudo apt install postgresql-12-postgis-scripts
```
3. This step populates the postgres db with functions from postgis and the spatial_ref_sys table. Run from the terminal
```
sudo -u postgres psql

CREATE EXTENSION adminpack;

sudo -u postgres psql

\connect postgres;

ALTER DATABASE postgres SET search_path=public, postgis, contrib;

\connect postgres;
CREATE EXTENSION postgis SCHEMA public;
SELECT postgis_full_version();
```
Output should give something like this:
```
                                                                                           postgis_full_version

------------------------------------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------
 POSTGIS="2.4.4 r16526" PGSQL="100" GEOS="3.6.2-CAPI-1.10.2 4d2925d6" PROJ="Rel. 4.9.3, 15 August 2016" GDAL="GDAL 2.2.3, released 2017/11/20" LIBXML=
"2.9.4" LIBJSON="0.12.1" LIBPROTOBUF="1.2.1" RASTER
```
Additionally, the postgres db should now have a spatial_ref_sys table and PostGis functions
