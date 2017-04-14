#!/usr/bin/python

__author__ = "Joseph Mullen"

import os
import subprocess as _sp

rootdir = "/Users/joemullen/Desktop/JIBfinalNtriples/"
sparql = 'http://localhost:8890/sparql-graph-crud-auth'
#sparql = 'http://drenin.ncl.ac.uk:8890/sparql-graph-crud-auth'
rdfconvertpath = "/Applications/rdfconvert-0.4/bin/"
limit = 10000
tmpfolder = os.path.dirname(os.path.abspath(__file__)) + "/tmp/"


def add_data(infile, usr, pwd, gpuri, store, overwrite=False):
    if overwrite == False:
        rqmethod = 'POST'
    elif overwrite == True:
        rqmethod = 'PUT'
    else:
        raise Exception('Invalid argument given for keyword "overwrite".')

    command = [
        'curl', '--digest', '-X',
        rqmethod, '--user',
        '{}:{}'.format(usr, pwd), '-G', store, '--data-urlencode', 'graph-uri={}'.format(gpuri), '-v', '-T',
        '{}'.format(infile), '--globoff'
    ]

    print str(command)

    _sp.call(command)


def streamed_upload():
    count = 0
    # go through the folder
    tmpfile = os.path.join(tmpfolder, "temp.rdf")
    # split the file(s)
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            if not file.startswith('.DS'):
                print os.path.join(subdir, file)
                command = split_command(os.path.join(subdir, file), tmpfolder)
                print command
                _sp.call(command, shell=True)
                upload_files()


def upload_files():
    # convert to rdf
    for subdir, dirs, files in os.walk(tmpfolder):
        for file in files:
            quick_check(os.path.join(subdir, file))
            command = convert_command(os.path.join(subdir, file), os.path.join(subdir,file) + ".rdf")
            print command
            _sp.call(command, shell=True, cwd=rdfconvertpath)
            # add data to database
            add_data(os.path.join(subdir, file)+".rdf", 'dba', 'dba', 'http://drenin', sparql)
            # remove the files
            delete_files(os.path.join(subdir, file))



def delete_graph(usr, pwd, gpuri, store):
    command = [
        'curl', '--digest', '-X', 'DELETE', '--user',
        '{}:{}'.format(usr, pwd), '-G', store, '--data-urlencode', 'graph-uri={}'.format(gpuri), '-v']

    print str(command)

    _sp.call(command)


'''Create the commands'''

def convert_command(fileFrom, fileTo):
    return '{} {} {}'.format("./rdfconvert.sh --input=N-Triples", fileFrom, fileTo)

def quick_check(file):
    command = sed_command("http://ncl.ac.uk/drenin#", "http://drenin.ncl.ac.uk/Terms#", os.path.join(file))
    _sp.call(command, shell=True)

# for the server remove the '' after sed
def sed_command(fromString, toString, file):
    return '{}{}{}{}{} {}'.format("sed -i '' \'s$", fromString, "$",toString, "$g\'",file)

def split_command(file, folder):
    return '{}{}{} {}'.format('split -l 60000 \'', file, "\'", folder)

def delete_files(filename):
    print 'deleting...\t' +filename
    # remove n-triple
    os.remove(filename)
    # remove the rdf
    os.remove(filename+".rdf")

streamed_upload()

# delete_graph('dba', 'dba', 'http://drenin', 'http://localhost:8890/sparql-graph-crud-auth')

