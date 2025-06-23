
import geopandas as gpd
from sqlalchemy import create_engine, text

#connect to the database
engine = create_engine("postgresql://postgres:pepper@localhost:5432/greater_sydney")

#drop tables with CASCADE if they exist
with engine.begin() as conn:
    conn.execute(text("DROP TABLE IF EXISTS sa2_boundaries CASCADE"))
    conn.execute(text("DROP TABLE IF EXISTS catchments_primary CASCADE"))
    conn.execute(text("DROP TABLE IF EXISTS catchments_secondary CASCADE"))
    conn.execute(text("DROP TABLE IF EXISTS catchments_future CASCADE"))

#load sa2 boundaries shapefile
sa2 = gpd.read_file("/Users/shrikha/greater_sydney/sa2_cleaned.shp")
#upload to table called sa2_boundaries
sa2.to_postgis("sa2_boundaries", engine, if_exists="replace", index=False)

#primary school catchments
primary = gpd.read_file("/Users/shrikha/greater_sydney/catchments_primary_cleaned.shp")
#save to postgres
primary.to_postgis("catchments_primary", engine, if_exists="replace", index=False)

#secondary school catchments
secondary = gpd.read_file("/Users/shrikha/greater_sydney/catchments_secondary_cleaned.shp")
#save to postgres
secondary.to_postgis("catchments_secondary", engine, if_exists="replace", index=False)

#future school catchments
future = gpd.read_file("/Users/shrikha/greater_sydney/catchments_future_cleaned.shp")
#upload to postgres
future.to_postgis("catchments_future", engine, if_exists="replace", index=False)

#add primary key to sa2_boundaries and recreate foreign key constraints
with engine.begin() as conn:
    #first add primary key to sa2_boundaries
    conn.execute(text("""
    DO $$
    BEGIN
        IF EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'sa2_boundaries') THEN
            ALTER TABLE sa2_boundaries ADD PRIMARY KEY (sa2_code);
        END IF;
    END
    $$;
    """))
    
    #recreate population foreign key if the table exists
    conn.execute(text("""
    DO $$
    BEGIN
        IF EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'population') THEN
            ALTER TABLE population 
            ADD CONSTRAINT population_sa2_code_fkey 
            FOREIGN KEY (sa2_code) REFERENCES sa2_boundaries(sa2_code);
        END IF;
    END
    $$;
    """))
    
    #recreate businesses foreign key if the table exists
    conn.execute(text("""
    DO $$
    BEGIN
        IF EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'businesses') THEN
            ALTER TABLE businesses 
            ADD CONSTRAINT businesses_sa2_code_fkey 
            FOREIGN KEY (sa2_code) REFERENCES sa2_boundaries(sa2_code);
        END IF;
    END
    $$;
    """))

