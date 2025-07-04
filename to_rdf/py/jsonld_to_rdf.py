from rdflib import Graph
import json

g = Graph()
g.parse(r"C:\Users\shiho\Documents\Study\Unibo\LOD\aLODofTea\downloaded_metadata\invitation\edited_invitation_europeana_metadata_jsonld.json", format="json-ld")

g.serialize(destination="invitation_europeana_metadata_rdf.ttl", format="turtle")