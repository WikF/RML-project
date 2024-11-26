from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF

# Define namespaces
SCHEMA = Namespace("http://schema.org/")
DBO = Namespace("http://dbpedia.org/ontology/")
CHARACTER = Namespace("http://example.org/character/")

# Parse XML
import xml.etree.ElementTree as ET
tree = ET.parse("characters.xml")


root = tree.getroot()

# Create RDF graph
g = Graph()
g.bind("schema", SCHEMA)
g.bind("dbo", DBO)
g.bind("character", CHARACTER)

# Convert XML to RDF
for char in root.findall("character"):
    char_id = char.attrib["id"]
    subject = CHARACTER[char_id]
    g.add((subject, RDF.type, SCHEMA.Person))
    g.add((subject, SCHEMA.givenName, Literal(char.find("firstname").text)))
    if char.find("lastname") is not None:
        g.add((subject, SCHEMA.lastName, Literal(char.find("lastname").text)))
    g.add((subject, DBO.hairColor, Literal(char.find("hair").text)))

# Save RDF to file
g.serialize("output.ttl", format="turtle")

