import argparse
from google.cloud import bigquery
from google.api_core.exceptions import NotFound

# UPDATED: Returns raw Python values, not SQL strings
def get_dummy_value(field_type):
    if field_type == "STRING": return "masked"
    if field_type in ["INTEGER", "INT64"]: return 0
    if field_type in ["FLOAT", "FLOAT64"]: return 0.0
    if field_type == "BOOL": return False
    # BigQuery expects strings for dates in JSON loads
    if field_type in ["TIMESTAMP", "DATETIME"]: return "2000-01-01 00:00:00"
    if field_type == "DATE": return "2000-01-01"
    return None

def populate_ghost_data(project_id, target_dataset):
    client = bigquery.Client(project=project_id)
    
    # 1. Define Source
    source_project = "bigquery-public-data"
    source_dataset = "austin_bikeshare" 
    table_name = "bikeshare_stations" 

    print(f"👻 Starting Ghost Data Engine (Sandbox Mode)...")

    # 2. Create Target Dataset
    dataset_ref = f"{project_id}.{target_dataset}"
    try:
        client.get_dataset(dataset_ref)
        print(f"   ✅ Dataset {dataset_ref} exists.")
    except NotFound:
        print(f"   🛠️ Creating dataset {dataset_ref}...")
        ds = bigquery.Dataset(dataset_ref)
        ds.location = "US"
        client.create_dataset(ds)

    # 3. Get Schema
    source_full = f"{source_project}.{source_dataset}.{table_name}"
    target_full = f"{project_id}.{target_dataset}.{table_name}"
    
    try:
        table_obj = client.get_table(source_full)
    except NotFound:
        print(f"   ❌ Source table not found!")
        return

    # 4. Construct the Dummy Row (Python Dictionary)
    # This creates a JSON object: {"station_id": 0, "name": "masked", ...}
    dummy_row = {}
    for field in table_obj.schema:
        dummy_row[field.name] = get_dummy_value(field.field_type)

    # 5. Load the Data (This works in Free Tier!)
    print(f"   🚚 Uploading dummy data via Load Job...")
    
    job_config = bigquery.LoadJobConfig(
        schema=table_obj.schema,
        write_disposition="WRITE_TRUNCATE", # Overwrite table if exists
    )
    
    # We pass the list [dummy_row] to create a table with 1 row
    job = client.load_table_from_json(
        [dummy_row], 
        target_full, 
        job_config=job_config
    )
    
    job.result() # Wait for job to finish
    print(f"   ✅ SUCCESS! Ghost data populated in {target_full}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True)
    parser.add_argument("--dataset", required=True)
    args = parser.parse_args()
    
    populate_ghost_data(args.project, args.dataset)