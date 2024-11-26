import os

from airflow.sensors.filesystem import FileSensor
from rdflib import Graph
from SPARQLWrapper import SPARQLWrapper, POST, BASIC
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
import os

os.environ['NO_PROXY'] = '*'

# Define paths and settings
OUTPUT_DIR = '/path/to/output/directory'
FUSEKI_URL = "http://localhost:3030/characters/update"  # Replace 'characters' with your dataset name
USERNAME = "admin"  # Replace with your Fuseki username
PASSWORD = "5LYL9ezTIchXh7S"  # Replace with your Fuseki password

def load_and_insert_data():
    """
    Load RDF data from a Turtle file and insert into Jena/Fuseki via SPARQL.
    """

    rdf_graph = Graph()
    rdf_graph.parse("output.ttl", format="ttl")
    print(f"Loaded {len(rdf_graph)} triples from 'output.ttl'")

    # Prepare the SPARQL query to insert the RDF data
    sparql = SPARQLWrapper(FUSEKI_URL)
    sparql.setMethod(POST)
    sparql.setHTTPAuth(BASIC)
    sparql.setCredentials(USERNAME, PASSWORD)

    sparql.setQuery("""
    PREFIX schema: <http://schema.org/>
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX character: <http://example.org/character/>

    INSERT DATA {
    """ + rdf_graph.serialize(format="nt") + """
    }
    """)

    try:
        response = sparql.query()
        print("Data uploaded successfully!")
    except Exception as e:
        raise Exception(f"Failed to upload data: {e}")

    # Delete the processed file after insertion

# Airflow DAG setup
with DAG(
    'rdf_etl_pipeline_with_jena',
    default_args={
        'owner': 'airflow',
        'retries': 3,
    },
    description='ETL pipeline for RDF to Jena/Fuseki',
    schedule_interval='@hourly',  # Change as needed
    start_date=days_ago(1),
    catchup=False,
) as dag:

    # Task to monitor the watch directory for files
    # Task to monitor the watch directory for files
    watch_files_task = FileSensor(
        task_id="watch_rdf_files", filepath="output.ttl", deferrable=False
    )

    # Task to process each file found and load it to Jena/Fuseki
    process_task = PythonOperator(
        task_id='process_and_load_rdf',
        python_callable=load_and_insert_data,
    )

    # Task dependencies
    watch_files_task >> process_task
