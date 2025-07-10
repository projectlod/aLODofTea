# ======== Base ========= #

import csv
from rdflib import Graph, Namespace, URIRef, Literal

NS = {
    "bf": Namespace("http://id.loc.gov/ontologies/bibframe/"),
    "crm": Namespace("http://www.cidoc-crm.org/cidoc-crm/"),
    "dcterms": Namespace("http://purl.org/dc/terms/"),
    "edm": Namespace("http://www.europeana.eu/schemas/edm/"),
    "foaf": Namespace("http://xmlns.com/foaf/0.1/"),
    "gn": Namespace("http://www.geonames.org/ontology#"),
    "owl": Namespace("http://www.w3.org/2002/07/owl#"),
    "rdfs": Namespace("http://www.w3.org/2000/01/rdf-schema#"),
    "schema": Namespace("https://schema.org/"),
    "skos": Namespace("http://www.w3.org/2004/02/skos/core#"),
    "tea": Namespace("https://w3id.org/a-lod-of-tea#"),
    "wd": Namespace("https://www.wikidata.org/wiki/"),
    "rdf": Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#"),  
}

def init_graph():
    from rdflib import Graph
    g = Graph()
    for prefix, ns in NS.items():
        g.bind(prefix, ns)
    return g

def write_graph(graph, output_path):
    graph.serialize(destination=output_path, format="turtle")


# ======== Custumize ========= #

import csv
from rdflib import URIRef, Literal

# initialize graph
g = init_graph()

# read csv file
with open("full_description/japanese-bridge.csv", newline='', encoding='cp932')  as csvfile:
    reader = csv.DictReader(csvfile)
    row = next(reader)  

# create URI
subject = NS["tea"]["item_japanese-bridge"]

# mapping
g.add((subject, NS["rdf"]["type"], NS["crm"]["E22_Human-Made_Object"]))
g.add((subject, NS["owl"]["sameAs"], NS["wd"]["Q12858617"]))
g.add((subject, NS["crm"]["P102_has_title"], Literal(row["Title Text"])))
g.add((subject, NS["crm"]["P4_has_time-span"], Literal(row["Earliest Date"])))
g.add((subject, NS["crm"]["P4_has_time-span"], Literal(row["Latest Date"])))
g.add((subject, NS["crm"]["P94i_was_created_by"], NS["wd"]["Q926"]))
g.add((subject, NS["dcterms"]["spatial"], NS["crm"]["E53_Place"]))
g.add((subject, NS["dcterms"]["medium"], NS["crm"]["E57_Material"]))
g.add((subject, NS["crm"]["P50_has_current_keeper"], NS["foaf"]["Organization"]))
g.add((subject, NS["dcterms"]["source"], URIRef("https://www.nga.gov/artworks/74796-japanese-footbridge")))
g.add((subject, NS["crm"]["P190_has_symbolic_content"], NS["skos"]["Concept"]))
g.add((subject, NS["dcterms"]["isPartOf"], NS["wd"]["Q1189907"]))




# output
write_graph(g, "japanese-bridge.ttl")
