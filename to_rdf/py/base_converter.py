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