from rdflib import Graph
from SPARQLWrapper import SPARQLWrapper, POST, BASIC

# Load RDF data from a Turtle file
rdf_graph = Graph()
rdf_graph.parse("output.ttl", format="ttl")

print(f"Loaded {len(rdf_graph)} triples from 'output.ttl'")

# Fuseki endpoint configuration
fuseki_url = "http://localhost:3030/characters/update"  # Replace 'characters' with your dataset name
username = "admin"  # Replace with your Fuseki username
password = "5LYL9ezTIchXh7S"  # Replace with your Fuseki password

# Initialize SPARQLWrapper
sparql = SPARQLWrapper(fuseki_url)
sparql.setMethod(POST)
sparql.setHTTPAuth(BASIC)
sparql.setCredentials(username, password)

# Serialize the RDF graph and prepare SPARQL INSERT DATA query
sparql.setQuery("""
PREFIX schema: <http://schema.org/>
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX character: <http://example.org/character/>

INSERT DATA {
""" + rdf_graph.serialize(format="nt") + """
}
""")

# Execute the SPARQL Update query
try:
    response = sparql.query()
    print("Data uploaded successfully!")
except Exception as e:
    print(f"Failed to upload data: {e}")
