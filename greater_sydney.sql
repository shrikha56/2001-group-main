CREATE SCHEMA public;
SET search_path TO public;
CREATE EXTENSION postgis;

--drop section
DROP TABLE IF EXISTS income CASCADE;
DROP TABLE IF EXISTS population CASCADE;
DROP TABLE IF EXISTS businesses CASCADE;
DROP TABLE IF EXISTS stops CASCADE;
DROP TABLE IF EXISTS sa2_boundaries CASCADE;
DROP TABLE IF EXISTS catchments_primary CASCADE;
DROP TABLE IF EXISTS catchments_secondary CASCADE;
DROP TABLE IF EXISTS catchments_future CASCADE;

--create sa2 boundaries first
CREATE TABLE sa2_boundaries (
    sa2_code TEXT PRIMARY KEY,
    sa2_name TEXT,
    geometry GEOMETRY(MultiPolygon, 4326)
);

--create income table
CREATE TABLE income (
    sa2_code TEXT PRIMARY KEY,
    sa2_name TEXT,
    median_income NUMERIC,
    mean_income NUMERIC
);

--create population table
CREATE TABLE population (
    sa2_code TEXT PRIMARY KEY,
    sa2_name TEXT,
    age_0_4 INTEGER,
    age_5_9 INTEGER,
    age_10_14 INTEGER,
    age_15_19 INTEGER,
    age_20_24 INTEGER,
    age_25_29 INTEGER,
    age_30_34 INTEGER,
    age_35_39 INTEGER,
    age_40_44 INTEGER,
    age_45_49 INTEGER,
    age_50_54 INTEGER,
    age_55_59 INTEGER,
    age_60_64 INTEGER,
    age_65_69 INTEGER,
    age_70_74 INTEGER,
    age_75_79 INTEGER,
    age_80_84 INTEGER,
    age_85_plus INTEGER,
    total_population INTEGER,
    FOREIGN KEY (sa2_code) REFERENCES sa2_boundaries(sa2_code)
);

--create businesses table
CREATE TABLE businesses (
    sa2_code TEXT,
    sa2_name TEXT,
    industry_code TEXT,
    industry_name TEXT,
    total_businesses INTEGER,
    PRIMARY KEY (sa2_code, industry_code),
    FOREIGN KEY (sa2_code) REFERENCES sa2_boundaries(sa2_code)
);

--create stops table
CREATE TABLE stops (
    stop_id TEXT PRIMARY KEY,
    stop_name TEXT,
    stop_lat DOUBLE PRECISION,
    stop_lon DOUBLE PRECISION,
    geom GEOMETRY(Point, 4326)
);

--create catchments primary table
CREATE TABLE catchments_primary (
    id SERIAL PRIMARY KEY,
    school_name TEXT,
    geometry GEOMETRY(MultiPolygon, 4326)
);

--create catchments secondary table
CREATE TABLE catchments_secondary (
    id SERIAL PRIMARY KEY,
    school_name TEXT,
    geometry GEOMETRY(MultiPolygon, 4326)
);

--create catchments future table
CREATE TABLE catchments_future (
    id SERIAL PRIMARY KEY,
    school_name TEXT,
    geometry GEOMETRY(MultiPolygon, 4326)
);

--create spatial indexes
CREATE INDEX ON sa2_boundaries USING GIST (geometry);
CREATE INDEX ON catchments_primary USING GIST (geometry);
CREATE INDEX ON catchments_secondary USING GIST (geometry);
CREATE INDEX ON catchments_future USING GIST (geometry);

