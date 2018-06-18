# Maral Dadvar
#This code extracts further information from GND for the authors of Freimann collection who have an GND-ID assigned to them.
#15/01/2018
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

file = io.open('textfile-bhr.json','w' , encoding ='utf-8')

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

select distinct ?o ?name ?bd ?dd ?bl ?dl ?abs ?pub
FROM <http://maral.wisslab.org/graphs/bhr>
 where
{
 ?o skos:prefLabel ?name
  optional {?o jl:birthDate ?bd}
   optional {?o jl:deathDate ?dd}
    optional{ ?o jl:birthLocation ?bl }
    optional {?o jl:deathLocation ?dl}
  optional {?o jl:hasAbstract ?abs}
  optional {?o jl:hasPublication ?pub}

}

""")

sparql.setReturnFormat(XML)

results = sparql.query().convert()

for i in range(0,len(results.bindings)):

    uri = results.bindings[i]['o'].value
    name = results.bindings[i]['name'].value

    if 'bd' in results.bindings[i].keys():
        birth = results.bindings[i]['bd'].value
    else: birth="NA"

    if 'dd' in results.bindings[i].keys():
        death = results.bindings[i]['dd'].value
    else: death = "NA"

    if 'bl' in results.bindings[i].keys():
        blocation = results.bindings[i]['bl'].value
        blocation = blocation.replace('\n','')
    else: blocation = "NA"

    if 'dl' in results.bindings[i].keys():
        dlocation=results.bindings[i]['dl'].value
        dlocation = dlocation.replace('\n','')
    else: dlocation = "NA"

    if 'abs' in results.bindings[i].keys():
        abstract = results.bindings[i]['abs'].value
        abstract = abstract.replace('"','')
        abstract = abstract.replace('{','')
        abstract = abstract.replace('}','')
        abstract = abstract.replace('/','')
        abstract = abstract.replace('\n','')
        abstract = abstract.replace('\r','')
        abstract = re.sub( '\s+', ' ', abstract).strip()
    else: abstract = "NA"

    if 'pub' in results.bindings[i].keys():
        publication = results.bindings[i]['pub'].value
        publication=publication.replace('"','')
        publication=publication.replace('{','')
        publication=publication.replace('}','')
        publication=publication.replace('/','')
        publication=publication.replace('\n','')
        publication=publication.replace('\r','')
        publication = re.sub( '\s+', ' ', publication).strip()
    else: publication = "NA"

    index = '{' + '"index":' + '{"_id":"' + uri + '"}}'
    file.writelines(index + '\n')

    rest = '{' + '"Name":"' + name + '",' + '"birthDate":"' + birth + '",' + '"deathDate":"' + death + '",' + '"birthLocation":"' + blocation  +'",' + '"deathLocation":"' + dlocation + '"' + ',' + '"Abstract":"' + abstract + '"' + ',' + '"Publication":"' + publication + '"' + '}'
    file.writelines(rest + '\n')
file.close()







