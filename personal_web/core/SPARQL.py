#!/usr/bin/env python

from urllib2 import urlopen
from SPARQLWrapper import SPARQLWrapper, JSON, RDF, XML, Wrapper


class Results():
    def __init__(self, results):
        self.variables = results['head']['vars']

        resultlst = []
        for result in results['results']['bindings']:
            dct = {}
            for var in results['head']['vars']:
                dct[var] = result[var]['value']

            resultlst.append(dct)

        self.results = resultlst

    def __str__(self):
        string = ''

        for result in self.results:
            for var in self.variables:
                string += '{} : {}\t'.format(var, result[var])
            string += '\n'

        return string


class Endpoint():
    def __init__(self, url, allgraphs, guri):
        self.url = url
        self.allgraphs = allgraphs
        self.graphuri = guri


    def __str__(self):
        return 'SPARQL Endpoint: {}'.format(self.url)

    def query(self, query_string):
        '''
        Derived from http://stackoverflow.com/questions/28455850/sparql-query-json-error-from-bncf-endpoint
        '''

        if self.allgraphs:
            sparql = SPARQLWrapper(self.url)
        else:
            sparql = SPARQLWrapper(self.url, defaultGraph=self.graphuri)
        sparql.setReturnFormat(JSON)
        sparql.setQuery(query_string)
        request = sparql._createRequest()
        request.add_header('Accept', 'application/sparql-results+json')

        response = urlopen(request)
        res = Wrapper.QueryResult((response, sparql.returnFormat))
        results = res.convert()

        return Results(results).results
