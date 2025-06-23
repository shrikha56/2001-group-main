import pandas as pd
import geopandas as gpd
from pathlib import Path
import os

#load all the datasets
income = pd.read_csv("Income.csv")
population = pd.read_csv("Population.csv")
businesses = pd.read_csv("Businesses.csv")
stops = pd.read_csv("stops.csv")  

#define a function to clean the income dataset
def clean_income(df):
    #rename the column sa2_code21 to sa2_code to ensure consistency with other datasets 
    df_renamed = df.rename(columns={
        "sa2_code21": "sa2_code",
    })
    df_copy = df_renamed[["sa2_code", "sa2_name", "median_income", "mean_income"]].copy()
    #type cast the median_income and mean_income to numeric values and replace missing values with NaN
    df_copy["median_income"] = pd.to_numeric(df_copy["median_income"], errors="coerce")
    df_copy["mean_income"] = pd.to_numeric(df_copy["mean_income"], errors="coerce")
    return df_copy

#define a function to clean the population dataset
def clean_population(df):
    #renames all the columns 
    df_renamed = df.rename(columns={
        "0-4_people": "age_0_4",
        "5-9_people": "age_5_9",
        "10-14_people": "age_10_14",
        "15-19_people": "age_15_19",
        "20-24_people": "age_20_24",
        "25-29_people": "age_25_29",
        "30-34_people": "age_30_34",
        "35-39_people": "age_35_39",
        "40-44_people": "age_40_44",
        "45-49_people": "age_45_49",
        "50-54_people": "age_50_54",
        "55-59_people": "age_55_59",
        "60-64_people": "age_60_64",
        "65-69_people": "age_65_69",
        "70-74_people": "age_70_74",
        "75-79_people": "age_75_79",
        "80-84_people": "age_80_84",
        "85-and-over_people": "age_85_plus",
        "total_people": "total_population"
    })
    #converts all the values in the population columns to integers
    pop_cols = [col for col in df_renamed.columns if col.startswith("age_") or col == "total_population"]
    df_copy = df_renamed.copy()
    for col in pop_cols:
        df_copy[col] = pd.to_numeric(df_copy[col], errors="coerce").fillna(0).astype(int)
    return df_copy[["sa2_code", "sa2_name"] + pop_cols]
    
#define a function to clean the business dataset
def clean_businesses(df):
    #create a dataframe with the required columns - sa2_code, sa2_name, industry_code, total_businesses
    df_copy = df[[
        "sa2_code", "sa2_name", "industry_code", "industry_name", "total_businesses"
    ]].copy()
    #convert the total number of registered businesses to a numeric and replace missing values with NaN
    df_copy["total_businesses"] = pd.to_numeric(df_copy["total_businesses"], errors="coerce").fillna(0).astype(int)
    return df_copy

#define a function to clean the stops dataset
def clean_stops(df):
    #create a dataframe with the required columns - stop_id, stop_name, stop_lat, stop_lon
    df_copy = df[["stop_id", "stop_name", "stop_lat", "stop_lon"]].copy()
    #convert the latitude and longitude to numeric values and replace missing values with NaN
    df_copy["stop_lat"] = pd.to_numeric(df_copy["stop_lat"], errors="coerce")
    df_copy["stop_lon"] = pd.to_numeric(df_copy["stop_lon"], errors="coerce")
    return df_copy.dropna(subset=["stop_lat", "stop_lon"])

#define a function to clean the shapefile for the schools
def clean_catchments(file_path):
    #use the GeoPandas library to read the shapefile directly with the string path
    gdf = gpd.read_file(file_path)
    #create a school_name column from USE_DESC which contains the school description
    if 'USE_DESC' in gdf.columns:
        gdf = gdf.rename(columns={"USE_DESC": "school_name"})
    else:
        # If USE_DESC is not present, create a placeholder name using the filename
        base_name = Path(file_path).stem
        gdf['school_name'] = f"{base_name}_catchment"
    
    #keep only necessary columns
    gdf = gdf[[col for col in gdf.columns if col in ['school_name', 'geometry']]]
    
    #checks the coordinate reference system of the shapefile and converts if necessary
    if gdf.crs is not None and gdf.crs.to_epsg() != 4326:
        gdf = gdf.to_crs(epsg=4326)
    elif gdf.crs is None:
        # Set a default CRS if none is detected
        gdf.set_crs(epsg=4326, inplace=True)
    return gdf

#define a function to clean the shapefile for the sa2 regions
def clean_sa2_boundaries(file_path):
    #use the GeoPandas library to read the shapefile directly with the string path
    gdf = gpd.read_file(file_path)
    #filters to get data from "Greater Sydney" region
    gdf = gdf[gdf["GCC_NAME21"] == "Greater Sydney"].copy()
    #rename columns for consistency
    gdf = gdf[["SA2_CODE21", "SA2_NAME21", "geometry"]].rename(columns={
        "SA2_CODE21": "sa2_code",
        "SA2_NAME21": "sa2_name"
    })
    #checks the coordinate reference system of the shapefile and converts if necessary
    if gdf.crs is not None and gdf.crs.to_epsg() != 4326:
        gdf = gdf.to_crs(epsg=4326)
    elif gdf.crs is None:
        # Set a default CRS if none is detected
        gdf.set_crs(epsg=4326, inplace=True)
    return gdf

def main():
    print("Loading CSV datasets...")

    income = pd.read_csv("Income.csv")
    population = pd.read_csv("Population.csv")
    businesses = pd.read_csv("Businesses.csv")
    stops = pd.read_csv("stops.csv")
    print("CSVs loaded.")

    print("Cleaning CSV datasets...")
    income_cleaned = clean_income(income)
    population_cleaned = clean_population(population)
    businesses_cleaned = clean_businesses(businesses)
    stops_cleaned = clean_stops(stops)
    print("CSVs cleaned.")

    print("Loading shapefiles...")
    try:
        sa2 = clean_sa2_boundaries("SA2_2021_AUST_GDA2020.shp")
        print("SA2 shapefile loaded.")
        
        primary = clean_catchments("catchments_primary.shp")
        print("Primary catchments loaded.")
        
        secondary = clean_catchments("catchments_secondary.shp")
        print("Secondary catchments loaded.")
        
        future = clean_catchments("catchments_future.shp")
        print("Future catchments loaded.")

        print("All datasets cleaned and ready for use.")
        print("-" * 50)
        
        # Display sample data from each dataset
        print("\nSample Income Data:")
        print(income_cleaned.head(3))
        
        print("\nSample Population Data:")
        print(population_cleaned.head(3))
        
        print("\nSample Business Data:")
        print(businesses_cleaned.head(3))
        
        print("\nSample Stops Data:")
        print(stops_cleaned.head(3))
        
        print("\nSA2 Regions:")
        print(sa2[['sa2_code', 'sa2_name']].head(3))
        
        # Save all cleaned datasets
        save_cleaned_data(income_cleaned, population_cleaned, businesses_cleaned, stops_cleaned, sa2, primary, secondary, future)
        
    except Exception as e:
        print(f"Error loading shapefiles: {e}")

def save_cleaned_data(income_cleaned, population_cleaned, businesses_cleaned, stops_cleaned, sa2, primary, secondary, future):
    # Save cleaned csv datasets
    income_cleaned.to_csv("income_cleaned.csv", index=False)
    population_cleaned.to_csv("population_cleaned.csv", index=False)
    businesses_cleaned.to_csv("businesses_cleaned.csv", index=False)
    stops_cleaned.to_csv("stops_cleaned.csv", index=False)
    
    # Save cleaned shapefiles
    sa2.to_file("sa2_cleaned.shp")
    primary.to_file("catchments_primary_cleaned.shp")
    secondary.to_file("catchments_secondary_cleaned.shp")
    future.to_file("catchments_future_cleaned.shp")
    

if __name__ == "__main__":
    main()