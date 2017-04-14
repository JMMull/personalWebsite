Requirements.
	
	Web
		Flask
		SPARQLWrapper $ sudo pip install sparqlwrapper
	
	Virtuoso Open Source
		Ubuntu $ sudo apt install virtuoso-opensource
		Mac $ brew install virtuoso

Start virtuoso.
	Mac $ cd /usr/local/Cellar/virtuoso/7.2.4.2/var/lib/virtuoso/db/
	    $ virtuoso-t -f
		(Can now access the Virtuoso front end at http://localhost:8890)
	Ubuntu 
	    $ 
Stop virtuoso.
	Mac
	    $ isql #to start an SQP prompt
	    $ SHUTDOWN;
	Ubuntu

Upload triples command line.

/sparql-graph-crud-auth (needed for read write access)
/sparql-graph-crud (read only access to the graph store)

#LOCAL	
curl --digest -X PUT --user dba:dba -H Content-Type:application/rdf+xml -G http://localhost:8890/sparql-graph-crud-auth --data-urlencode graph-uri=http://drenin -v -T DReNIn_Ontology.owl

curl -v -T DReNIn_v1.1_Protein---has_molecular_function-.nt http://drenin.ncl.ac.uk:8890/sparql-graph-crud?graph-uri=http://drenin -u dba:dba

#SERVER
ssh into server— add from there.
	
curl --digest -X PUT --user dba:dba -H Content-Type:application/rdf+xml -G http://drenin.ncl.ac.uk:8890/sparql-graph-crud-auth --data-urlencode graph-uri=http://drenin -v -T DReNIn_Ontology.owl

curl --digest -X PUT --user dba:dba -H Content-Type:application/rdf+xml -G http://drenin.ncl.ac.uk:8890/sparql-graph-crud-auth --data-urlencode graph-uri=http://drenin -v -T DReNIn_v1.1_Small_Molecule---has_side_effect-.nt 

Query (using the UI).

#Download data from a  given graph:
curl -G http://localhost:8890/sparql-graph-crud --data-urlencode graph=http://drenin > here.txt

#DELETE a graph
curl -X DELETE --digest -u dba:dba -G http://localhost:8890/sparql-graph-crud-auth --data-urlencode graph=http://drenin


#DELETE ALL TRIPLES APART FROM SYSTEM triples from the viruoso server
go to the iSQL (via conductor @8890) and $ SQL> RDF_GLOBAL_RESET ();

1. using command line- curl…. 
	http://drenin.ncl.ac.uk:8890/sparql?default-graph-uri=http%3A%2F%2Fdrenin&query=select+%3Fs+%3Fp+%3Fo+WHERE+%7B%3Fs+%3Fp+%3Fo%7D&should-sponge=&format=text%2Fhtml&timeout=0&debug=on

	    http://localhost:8890/sparql

Simple.
	    select ?s ?p ?o WHERE {?s ?p ?o}


POPULATE DATABASE:
cd /DReNIn_Web/drenin_web/core/
$ populatevirtuoso.py


PRODUCTION READY.

# install uwsgi
sudo pip install uwsgi
# install nginx
sudo apt-get install nginx

# also need to change the ssymlink pointing to the default 'site' in nginx
$ cd /etc/nginx/
$ ls sites-enabled/
$ rm -rf sites-enabled/default
$ sudo rm -rf sites-enabled/default
# need to make a few changes to the nginx conf //sudo vi /etc/nginx/nginx.conf

run:
$ uwsgi --ini drenin-uwsgi.ini &
OR
$ uwsgi --http :5000 --wsgi-file run.py --callable app &
