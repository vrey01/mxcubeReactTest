"""
Simple demonstration of how to implement Server-sent events (SSE) in Python
using Bottle micro web-framework.
 
SSE require asynchronous request handling, but it's tricky with WSGI. One way
to achieve that is to use gevent library as shown here.
 
Usage: just start the script and open http://localhost:8080/ in your browser.
 
Based on:
- "Primer to Asynchronous Applications",
     http://bottlepy.org/docs/dev/async.html

- "Using server-sent events",
     https://developer.mozilla.org/en-US/docs/Server-sent_events/Using_server-sent_events
"""
 
# Bottle requires gevent.monkey.patch_all() even if you don't like it.
import time, os,sys
import json
import socket

from gevent import monkey; monkey.patch_all()
from gevent import sleep
 
import bottle
from bottle import get, post, request, response, route, static_file, redirect
from bottle import GeventServer, run

from beaker.middleware import SessionMiddleware

samples_info="""{'status': {'code': 'ok'}, 'loaded_sample': [ {'holderLength': 22.0, 'code': None, 'containerSampleChangerLocation': '1', 'proteinAcronym': 'Mnth', 'cellGamma': 0.0, 'cellAlpha': 0.0, 'sampleId': 444178, 'cellBeta': 0.0, 'crystalSpaceGroup': 'R32', 'sampleLocation': '1', 'sampleName': 'sample-E01', 'cellA': 0.0, 'diffractionPlan': {}, 'cellC': 0.0, 'cellB': 0.0, 'experimentType': 'Default'}, 
{'holderLength': 22.0, 'code': None, 'containerSampleChangerLocation': '1', 'proteinAcronym': 'Mnth', 'cellGamma': 0.0, 'cellAlpha': 0.0, 'sampleId': 444179, 'cellBeta': 0.0, 'crystalSpaceGroup': 'R32', 'sampleLocation': '2', 'sampleName': 'sample-E02', 'cellA': 0.0, 'diffractionPlan': {}, 'cellC': 0.0, 'cellB': 0.0, 'experimentType': 'Default'}, {'holderLength': 22.0, 'code': None, 'containerSampleChangerLocation': '1', 'proteinAcronym': 'Mnth', 'cellGamma': 0.0, 'cellAlpha': 0.0, 'sampleId': 444180, 'cellBeta': 0.0, 'crystalSpaceGroup': 'R32', 'sampleLocation': '3', 'sampleName': 'sample-E03', 'cellA': 0.0, 'diffractionPlan': {}, 'cellC': 0.0, 'cellB': 0.0, 'experimentType': 'Default'}, {'holderLength': 22.0, 'code': None, 'containerSampleChangerLocation': '1', 'proteinAcronym': 'Mnth', 'cellGamma': 0.0, 'cellAlpha': 0.0, 'sampleId': 444181, 'cellBeta': 0.0, 'crystalSpaceGroup': 'R32', 'sampleLocation': '4', 'sampleName': 'sample-E04', 'cellA': 0.0, 'diffractionPlan': {
}, 'cellC': 0.0, 'cellB': 0.0, 'experimentType': 'Default'}, {'holderLength': 22.0, 'code': None, 'containerSampleChangerLocation': '1', 'proteinAcronym': 'Mnth', 'cellGamma': 0.0, 'cellAlpha': 0.0, 'sampleId': 444182, 'cellBeta': 0.0, 'crystalSpaceGroup': 'R32', 'sampleLocation': '5', 'sampleName': 'sample-E05', 'cellA': 0.0, 'diffractionPlan': {
'diffractionPlanId' : 266042,
'experimentKind' : "Default",
'exposureTime' : 0.0,
}, 'cellC': 0.0, 'cellB': 0.0, 'experimentType': 'Default'}, {'holderLength': 22.0, 'code': None, 'containerSampleChangerLocation': '1', 'proteinAcronym': 'Mnth', 'cellGamma': 0.0, 'cellAlpha': 0.0, 'sampleId': 444183, 'cellBeta': 0.0, 'crystalSpaceGroup': 'R32', 'sampleLocation': '6', 'sampleName': 'sample-E06', 'cellA': 0.0, 'diffractionPlan': {
}, 'cellC': 0.0, 'cellB': 0.0, 'experimentType': 'Default'}, {'holderLength': 22.0, 'code': None, 'containerSampleChangerLocation': '1', 'proteinAcronym': 'Mnth', 'cellGamma': 0.0, 'cellAlpha': 0.0, 'sampleId': 444184, 'cellBeta': 0.0, 'crystalSpaceGroup': 'R32', 'sampleLocation': '7', 'sampleName': 'sample-E07', 'cellA': 0.0, 'diffractionPlan': {
}, 'cellC': 0.0, 'cellB': 0.0, 'experimentType': 'Default'}, {'holderLength': 22.0, 'code': None, 'containerSampleChangerLocation': '1', 'proteinAcronym': 'Mnth', 'cellGamma': 0.0, 'cellAlpha': 0.0, 'sampleId': 444185, 'cellBeta': 0.0, 'crystalSpaceGroup': 'R32', 'sampleLocation': '8', 'sampleName': 'sample-E08', 'cellA': 0.0, 'diffractionPlan': {
}, 'cellC': 0.0, 'cellB': 0.0, 'experimentType': 'Default'}, {'holderLength': 22.0, 'code': None, 'containerSampleChangerLocation': '1', 'proteinAcronym': 'Mnth', 'cellGamma': 0.0, 'cellAlpha': 0.0, 'sampleId': 444186, 'cellBeta': 0.0, 'crystalSpaceGroup': 'R32', 'sampleLocation': '9', 'sampleName': 'sample-E09', 'cellA': 0.0, 'diffractionPlan': {
}, 'cellC': 0.0, 'cellB': 0.0, 'experimentType': 'Default'}, {'holderLength': 22.0, 'code': None, 'containerSampleChangerLocation': '1', 'proteinAcronym': 'Mnth', 'cellGamma': 0.0, 'cellAlpha': 0.0, 'sampleId': 444187, 'cellBeta': 0.0, 'crystalSpaceGroup': 'R32', 'sampleLocation': '10', 'sampleName': 'sample-E10', 'cellA': 0.0, 'diffractionPlan': {
}, 'cellC': 0.0, 'cellB': 0.0, 'experimentType': 'Default'}]}"""

session_opts = {
    'session.type': 'file',
    'session.cookie_expires': 300,
    'session.data_dir': './data',
    'session.auto': True
}

app = SessionMiddleware(bottle.app(), session_opts)

@get('/samples')
def return_samples():
    return json.dumps(eval(samples_info))

@post('/sample_field_update')
def sample_field_update():
    print "Sample field updated"
    print request.POST.items()
    return 

@get("/")
@get("/login")
def login():
    if 'proposal' in request.GET.keys() and request.GET['proposal'] != "":
        remaddr = request.environ['REMOTE_ADDR']
        try:
          remhost = socket.gethostbyaddr( remaddr )[0]
          localhost = socket.gethostname() 
          if True: #remhost  in ['localhost', localhost]:
             successful_login(request.GET)
             response.status=303
             response.set_header("location","/mxcube")
             return
        except:
          sys.excepthook(*sys.exc_info())
        
        # exception or remote
        redirect('http://www.google.com')
    else:
        return static_file("login.html", os.path.dirname(__file__))

@route("/mxcube/proposal")
def mxcube_proposal():
    sess = request.environ.get('beaker.session')
    return { "proposal": sess.get("proposal", "") }

@get("/logout")
def logout():
    sess = request.environ.get('beaker.session')
    sess.delete()
    response.status=303
    response.set_header("location","/login")

def successful_login( getdict ):
    sess = request.environ.get('beaker.session')
    sess['proposal'] = getdict['proposal']
    sess.save()

@route("/mxcube")
def mxcube():
    sess = request.environ.get('beaker.session')

    return static_file("mxcube.html", os.path.dirname(__file__))

@route("/sample_list")
def sample_list():
   return static_file("samples_test.html", os.path.dirname(__file__))

@route("/<url:path>")
def serve_static_file(url):
   return static_file(url, os.path.dirname(__file__))

if __name__ == '__main__':
    run(app=app, host="", port="8080",server=GeventServer)
