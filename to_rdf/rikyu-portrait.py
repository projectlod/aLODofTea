"""
CSV to RDF Converter for CIDOC-CRM metadata
Transforms CSV data into RDF (Turtle format) using rdflib
"""

import csv
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS, DCTERMS, SKOS, OWL

# Initialize RDF graph with namespaces
g = Graph()

# Define namespaces
BASE = Namespace("https://w3id.org/a-lod-of-tea/")
CRM = Namespace("http://www.cidoc-crm.org/cidoc-crm/")
WD = Namespace("https://www.wikidata.org/wiki/")
SCHEMA = Namespace("https://schema.org/")

# Bind namespaces to prefixes
g.bind("base", BASE)
g.bind("crm", CRM)
g.bind("dcterms", DCTERMS)
g.bind("skos", SKOS)
g.bind("schema", SCHEMA)
g.bind("owl", OWL)
g.bind("wd", WD)

# Input and output files
input_file = r"C:\Users\shiho\Documents\Study\Unibo\LOD\aLODofTea\rdf_transformation\rikyu-portrait.csv"
output_file = r"C:\Users\shiho\Documents\Study\Unibo\LOD\aLODofTea\rdf_transformation\rikyu-portrait.ttl"

print("Starting CSV to RDF conversion...")
print(f"Input file: {input_file}")
print(f"Output file: {output_file}")

# Read CSV file using built-in csv module
with open(input_file, 'r', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    row_count = 0   
    
    # Process each row
    for row in reader:
        row_count += 1
        subject_str = row['subject']
        predicate_str = row['predicate']
        object_str = row['object']
        
        # Skip rows with empty predicates or objects
        if not predicate_str or not object_str or predicate_str.strip() == "" or object_str.strip() == "":
            continue
        
        # Create subject URI using base namespace
        subject = BASE[subject_str]
        
        # Parse predicate string to extract namespace and property
        predicate_str = predicate_str.strip()
        predicate = None
        
        if predicate_str.startswith("dcterms:"):
            predicate = DCTERMS[predicate_str.split(":")[1].strip()]
        elif predicate_str.startswith("crm:"):
            predicate = CRM[predicate_str.split(":")[1]]
        elif predicate_str.startswith("skos:"):
            predicate = SKOS[predicate_str.split(":")[1]]
        elif predicate_str.startswith("schema:"):
            predicate = SCHEMA[predicate_str.split(":")[1]]
        elif predicate_str.startswith("owl:"):
            predicate = OWL[predicate_str.split(":")[1]]
        else:
            # If no namespace prefix, assume it's a CRM property
            predicate = CRM[predicate_str]
        
        if predicate is None:
            continue
        
        # Parse object string to determine if it's a URI or literal
        object_str = object_str.strip()
        obj = None
        
        # Check if it's a Wikidata URI
        if object_str.startswith("https://www.wikidata.org/wiki/"):
            # Extract the Wikidata ID and create prefixed URI
            wd_id = object_str.split("/")[-1]
            obj = WD[wd_id]
        # Check if it's any other URI
        elif object_str.startswith("http://") or object_str.startswith("https://"):
            obj = URIRef(object_str)
        # Otherwise, treat as literal
        else:
            obj = Literal(object_str)
        
        if obj is None:
            continue
        
        # Add triple to graph
        g.add((subject, predicate, obj))
        print(f"Added triple: {subject} {predicate} {obj}")

print(f"Successfully loaded CSV with {row_count} rows")

# Serialize graph to Turtle format
ttl_data = g.serialize(format='turtle')

# Write to file
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(ttl_data)

print(f"Successfully converted CSV to RDF. Output saved to: {output_file}")
print(f"Total triples created: {len(g)}")

# Display a preview of the generated RDF
print("\nFirst few lines of generated RDF:")
with open(output_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for i, line in enumerate(lines[:20]):  # Show first 20 lines
        print(line.rstrip())
    if len(lines) > 20:
        print("...")

print("\nConversion completed successfully!")