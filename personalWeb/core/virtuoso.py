#!/usr/bin/env python
import os
import sys
import urllib
import subprocess as _sp
import personal_web.core.SPARQL as query

sys.path.append(os.path.abspath('../..'))


class Repository():
    def __init__(self, user, password, store, graphuri, endpoint, allgraphs):
        self.usr = user
        self.pwd = password
        self.store = store
        self.gpuri = graphuri
        self.endpoint = endpoint
        self.allgraphs = allgraphs

    def __str__(self):
        return 'User: {}\nPass: {}\nStore: {}\nGraph URI: {}'.format(
            self.usr,
            self.pwd,
            self.store,
            self.gpuri)

    def update_graph(self, new_graph):
        self.gpuri = new_graph

    def add_data(self, infile, overwrite=False):
        if overwrite == False:
            rqmethod = 'POST'
        elif overwrite == True:
            rqmethod = 'PUT'
        else:
            raise Exception('Invalid argument given for keyword "overwrite".')

        command = [
            'curl', '--digest', '--user',
            '{}:{}'.format(self.usr, self.pwd), '--verbose', '--url',
            '{}?graph-uri={}'.format(self.store, self.gpuri), '-X',
            rqmethod, '-T', '{}'.format(infile)
        ]

        _sp.call(command)

    def query(self):
        command = [
            'curl', '--digest', '--user',
            '{}:{}'.format(self.usr, self.pwd), '--verbose', '--url',
            '{}?graph-uri={}'.format(self.store, self.gpuri)
        ]

        print command

        _sp.call(command)

    def delete(self):
        command = [
            'curl', '--digest', '--user',
            '{}:{}'.format(self.usr, self.pwd), '--verbose', '--url',
            '{}?graph-uri={}'.format(self.store, self.gpuri), '-X'
                                                              'DELETE']

        _sp.call(command)

    def sparql_query(self, q):
        print self.allgraphs
        endpoint = query.Endpoint(self.endpoint, self.allgraphs, self.gpuri)
        lst = []
        start = 0
        while True:
            run = False
            while run == False:
                try:
                    qrun = q + '\n OFFSET {}'.format(start)
                    results = endpoint.query(qrun)
                    lst += results
                    run = True
                except Exception as E:
                    if str(E) == 'HTTP Error 500: SPARQL Request Failed':
                        pass
                    else:
                        raise Exception()

            if len(results) < 10000:
                break
            start += 10000

        return lst
