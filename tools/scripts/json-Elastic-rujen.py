# Maral Dadvar
#This code transformes the rujen dataset generated for JudaicaLink into the format adaptable to Elasticsearch.
#28/05/2018
#Ver. 01

import rdflib
from rdflib import Namespace, URIRef, Graph , Literal
from SPARQLWrapper import SPARQLWrapper2, XML , RDF , JSON
from rdflib.namespace import RDF, FOAF , SKOS ,RDFS
import os
import json
import io
import re

os.chdir('C:\Users\Maral\Desktop')

sparql = SPARQLWrapper2("http://localhost:3030/Datasets/sparql")

file = io.open('textfile-rujen.json','w' , encoding ='utf-8')

foaf = Namespace("http://xmlns.com/foaf/0.1/")
skos = Namespace("http://www.w3.org/2004/02/skos/core#")
gndo = Namespace("http://d-nb.info/standards/elementset/gnd#")
jl = Namespace("http://data.judaicalink.org/ontology/")
owl = Namespace ("http://www.w3.org/2002/07/owl#")



sparql.setQuery("""
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX gndo: <http://d-nb.info/standards/elementset/gnd#>
    PREFIX pro: <http://purl.org/hpi/patchr#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX edm: <http://www.europeana.eu/schemas/edm/>
    PREFIX dc: <http://purl.org/dc/elements/1.1/>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX dblp: <http://dblp.org/rdf/schema-2015-01-26#>
    PREFIX dcterms: <http://purl.org/dc/terms/>
    PREFIX bibtex: <http://data.bibbase.org/ontology/#>
    PREFIX jl: <http://data.judaicalink.org/ontology/>

select distinct ?o ?name ?abs (group_concat(?alt; SEPARATOR="-") as ?alt2)

where
{
  graph <http://maral.wisslab.org/graphs/rujen> {

    ?o a skos:Concept.
    ?o skos:prefLabel ?name.
    ?o skos:altLabel ?alt.
    ?o jl:hasAbstract ?abs

    }
} group by ?o ?name ?abs


""")

sparql.setReturnFormat(XML)

results = sparql.query().convert()

for i in range(0,len(results.bindings)):

    uri = results.bindings[i]['o'].value
    name = results.bindings[i]['name'].value


    if 'abs' in results.bindings[i].keys():
        abstract = results.bindings[i]['abs'].value
        abstract = abstract.replace('"','')
        abstract = abstract.replace('{','')
        abstract = abstract.replace('}','')
        abstract = re.sub( '\s+', ' ', abstract).strip()
    else: abstract = "NA"

    if 'alt2' in results.bindings[i].keys():
        altname = results.bindings[i]['alt2'].value
        altname = altname.replace('{','')
        altname = altname.replace('}','')
        altname = altname.replace('"','')
        altname = altname.replace('.','')
    else: altname = "NA"

    index = '{' + '"index":' + '{"_id":"' + uri + '"}}'
    file.writelines(index + '\n')

    rest = '{' + '"Name":"' + name + '",' + '"Alternatives":"' + altname  +'",' + '"Abstract":"' + abstract + '"' '}'
    file.writelines(rest + '\n')
file.close()







