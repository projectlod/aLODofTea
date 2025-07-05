from rdflib import Graph
import os
import glob

ttl_files = glob.glob(r"C:\Users\shiho\Documents\Study\Unibo\LOD\aLODofTea\to_rdf\ttl\*.ttl")

merged_graph = Graph()
for file in ttl_files:
    merged_graph.parse(file, format="turtle")

merged_graph.serialize(destination=r"C:\Users\shiho\Documents\Study\Unibo\LOD\aLODofTea\to_rdf\ttl\full_dataset.ttl", format="turtle")


print(f"Merged {len(ttl_files)} files into 'full_dataset.ttl'")
