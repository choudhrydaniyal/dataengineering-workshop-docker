import pandas as pd
from sqlalchemy import create_engine

dtype = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64"
}

parse_dates = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]

def run_ingestion(year: int, month: int, pg_user: str, pg_password: str, pg_host: str, pg_port: str, pg_database: str, url: str, table_name: str, chunk_size: int, engine = None):
    print(f"Downloading data from {url}...")
    df = pd.read_csv(url, dtype=dtype, parse_dates=parse_dates)

    print(f"Creating iterator for reading data in chunks of size {chunk_size}...")
    df_iter = pd.read_csv(
        url,
        dtype = dtype,
        parse_dates = parse_dates,
        iterator = True,
        chunksize = chunk_size
    )

    first = True

    for df_chunk in df_iter:
        if first:
            print(f"Creating table {table_name} in the database...")
            df_chunk.head(0).to_sql(name = table_name, con = engine, if_exists = 'replace')
            first = False
        print(f"Inserting chunk into the database...")
        df_chunk.to_sql(name = table_name, con = engine, if_exists = 'append')
    
    print("Data ingestion completed.")


def main():
    pg_user = "root"
    pg_password = "root"
    pg_host = "localhost"
    pg_port = "5432"
    pg_database = "ny_taxi"
    year = 2021
    month = 1
    url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_{year}-{month:02d}.csv.gz"
    table_name = "yellow_taxi_data"
    chunk_size = 10000

    engine = create_engine(f"postgresql://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_database}")

    run_ingestion(year, month, pg_user, pg_password, pg_host, pg_port, pg_database, url, table_name, chunk_size, engine)

if __name__ == '__main__':
    main()
