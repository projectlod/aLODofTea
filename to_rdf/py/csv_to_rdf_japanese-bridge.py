"""
CSV to RDF Converter for CIDOC-CRM metadata
Transforms CSV data into RDF (Turtle format) using rdflib.
Before implementation, store the csv file under folder : /to_rdf/csv
After implementation, save the this .py file under folder : /to_rdf/py with the name of the item
"""

import csv
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS, DCTERMS, SKOS, OWL, FOAF

#Initialize RDF graph
g = Graph()

# Define namespaces
TEA = Namespace("https://w3id.org/a-lod-of-tea#")  
CRM = Namespace("http://www.cidoc-crm.org/cidoc-crm/")
WD = Namespace("https://www.wikidata.org/wiki/")
SCHEMA = Namespace("https://schema.org/")
DCTERMS = Namespace("http://purl.org/dc/terms/")
SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")
OWL = Namespace("http://www.w3.org/2002/07/owl#")
RDF = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
FOAF = Namespace("http://xmlns.com/foaf/0.1/")
EDM = Namespace("http://www.europeana.eu/schemas/edm/")
BF = Namespace("http://id.loc.gov/ontologies/bibframe/")
GN = Namespace("http://www.geonames.org/ontology#")

# Bind namespaces with prefixes
g.bind("tea", TEA)
g.bind("crm", CRM)
g.bind("wd", WD)
g.bind("schema", SCHEMA)
g.bind("dcterms", DCTERMS)
g.bind("skos", SKOS)
g.bind("owl", OWL)
g.bind("rdf", RDF)
g.bind("rdfs", RDFS)
g.bind("foaf", FOAF)
g.bind("edm", EDM)
g.bind("bf", BF)
g.bind("gn", GN)

# Namespace mapping for easier access
NAMESPACE_MAP = {
    "dcterms": DCTERMS, "crm": CRM, "skos": SKOS, "schema": SCHEMA,
    "owl": OWL, "rdf": RDF, "rdfs": RDFS, "foaf": FOAF,
    "edm": EDM, "bf": BF, "gn": GN, "wd": WD, "tea": TEA
}

# File paths - chang these according to your local environment
input_file = r"C:\Users\shiho\Documents\Study\Unibo\LOD\aLODofTea\to_rdf\csv\japanese-bridge.csv"

# save under /to_rdf/ttl, with the name of the item. if it already exists, it will be overwritten
output_file = r"C:\Users\shiho\Documents\Study\Unibo\LOD\aLODofTea\to_rdf\ttl\japanese-bridge.ttl"  

# Convert CSV to RDF
print("Converting CSV to RDF...")


with open(input_file, 'r', encoding='utf-8-sig') as csvfile: #if this doesn't work, try encoding='utf-8' or  encoding='latin-1'
    reader = csv.DictReader(csvfile)
    
    for row in reader:
        subject_str = row.get('subject', '').strip()
        predicate_str = row.get('predicate', '').strip()
        object_str = row.get('object', '').strip()
        
        # Skip empty rows if any
        if not subject_str or not predicate_str or not object_str:
            continue
        
        # Parse subject (URI or prefixed URI)
        if ":" in subject_str:
            prefix, local_name = subject_str.split(":", 1)
            if prefix.strip() in NAMESPACE_MAP:
                subject = NAMESPACE_MAP[prefix.strip()][local_name.strip()]
            else:
                subject = TEA[subject_str]
        else:
            subject = TEA[subject_str]
        
        # Parse predicate (URI of a schema)
        if ":" in predicate_str:
            prefix, local_name = predicate_str.split(":", 1)
            predicate = NAMESPACE_MAP.get(prefix.strip(), CRM)[local_name.strip()]
        else:
            predicate = CRM[predicate_str]
        
        # Parse object (URI or literal)
        if object_str.startswith("http://") or object_str.startswith("https://"):
            # if the object has a wikidata URL format, extract the ID. Otherwise, treat it as a URI
            if object_str.startswith("https://www.wikidata.org/wiki/"):
                wd_id = object_str.split("/")[-1]
                obj = WD[wd_id]
            else:
                obj = URIRef(object_str)
        elif ":" in object_str:
            # Prefixed URI
            prefix, local_name = object_str.split(":", 1)
            if prefix.strip() in NAMESPACE_MAP:
                obj = NAMESPACE_MAP[prefix.strip()][local_name.strip()]
            else:
                obj = Literal(object_str)
        else:
            # Literal
            obj = Literal(object_str)
        
        # Add triple
        g.add((subject, predicate, obj))

# Save to file
ttl_data = g.serialize(format='turtle')
with open(output_file, 'w', encoding='utf-8-sig') as f:
    f.write(ttl_data)

print(f"Conversion completed! {len(g)} triples created.")
print(f"Output saved to: {output_file}")