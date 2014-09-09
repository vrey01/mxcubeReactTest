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

from gevent import monkey; monkey.patch_all()
from gevent import sleep
 
from bottle import get, post, request, response, route, static_file
from bottle import GeventServer, run

samples_info="""{'status': {'code': 'ok'}, 'loaded_sample': [{'holderLength': 22.0, 'code': None, 'containerSampleChangerLocation': '1', 'proteinAcronym': 'Mnth', 'cellGamma': 0.0, 'cellAlpha': 0.0, 'sampleId': 444178, 'cellBeta': 0.0, 'crystalSpaceGroup': 'R32', 'sampleLocation': '1', 'sampleName': 'sample-E01', 'cellA': 0.0, 'diffractionPlan': (diffractionPlanWS3VO){
diffractionPlanId = 266040
experimentKind = "Default"
exposureTime = 0.0
}, 'cellC': 0.0, 'cellB': 0.0, 'experimentType': 'Default'}, {'holderLength': 22.0, 'code': None, 'containerSampleChangerLocation': '1', 'proteinAcronym': 'Mnth', 'cellGamma': 0.0, 'cellAlpha': 0.0, 'sampleId': 444179, 'cellBeta': 0.0, 'crystalSpaceGroup': 'R32', 'sampleLocation': '2', 'sampleName': 'sample-E02', 'cellA': 0.0, 'diffractionPlan': (diffractionPlanWS3VO){
diffractionPlanId = 266041
experimentKind = "Default"
exposureTime = 0.0
}, 'cellC': 0.0, 'cellB': 0.0, 'experimentType': 'Default'}, {'holderLength': 22.0, 'code': None, 'containerSampleChangerLocation': '1', 'proteinAcronym': 'Mnth', 'cellGamma': 0.0, 'cellAlpha': 0.0, 'sampleId': 444180, 'cellBeta': 0.0, 'crystalSpaceGroup': 'R32', 'sampleLocation': '3', 'sampleName': 'sample-E03', 'cellA': 0.0, 'diffractionPlan': (diffractionPlanWS3VO){
diffractionPlanId = 266042
experimentKind = "Default"
exposureTime = 0.0
}, 'cellC': 0.0, 'cellB': 0.0, 'experimentType': 'Default'}, {'holderLength': 22.0, 'code': None, 'containerSampleChangerLocation': '1', 'proteinAcronym': 'Mnth', 'cellGamma': 0.0, 'cellAlpha': 0.0, 'sampleId': 444181, 'cellBeta': 0.0, 'crystalSpaceGroup': 'R32', 'sampleLocation': '4', 'sampleName': 'sample-E04', 'cellA': 0.0, 'diffractionPlan': (diffractionPlanWS3VO){
diffractionPlanId = 266043
experimentKind = "Default"
exposureTime = 0.0
}, 'cellC': 0.0, 'cellB': 0.0, 'experimentType': 'Default'}, {'holderLength': 22.0, 'code': None, 'containerSampleChangerLocation': '1', 'proteinAcronym': 'Mnth', 'cellGamma': 0.0, 'cellAlpha': 0.0, 'sampleId': 444182, 'cellBeta': 0.0, 'crystalSpaceGroup': 'R32', 'sampleLocation': '5', 'sampleName': 'sample-E05', 'cellA': 0.0, 'diffractionPlan': (diffractionPlanWS3VO){
diffractionPlanId = 266044
experimentKind = "Default"
exposureTime = 0.0
}, 'cellC': 0.0, 'cellB': 0.0, 'experimentType': 'Default'}, {'holderLength': 22.0, 'code': None, 'containerSampleChangerLocation': '1', 'proteinAcronym': 'Mnth', 'cellGamma': 0.0, 'cellAlpha': 0.0, 'sampleId': 444183, 'cellBeta': 0.0, 'crystalSpaceGroup': 'R32', 'sampleLocation': '6', 'sampleName': 'sample-E06', 'cellA': 0.0, 'diffractionPlan': (diffractionPlanWS3VO){
diffractionPlanId = 266045
experimentKind = "Default"
exposureTime = 0.0
}, 'cellC': 0.0, 'cellB': 0.0, 'experimentType': 'Default'}, {'holderLength': 22.0, 'code': None, 'containerSampleChangerLocation': '1', 'proteinAcronym': 'Mnth', 'cellGamma': 0.0, 'cellAlpha': 0.0, 'sampleId': 444184, 'cellBeta': 0.0, 'crystalSpaceGroup': 'R32', 'sampleLocation': '7', 'sampleName': 'sample-E07', 'cellA': 0.0, 'diffractionPlan': (diffractionPlanWS3VO){
diffractionPlanId = 266046
experimentKind = "Default"
exposureTime = 0.0
}, 'cellC': 0.0, 'cellB': 0.0, 'experimentType': 'Default'}, {'holderLength': 22.0, 'code': None, 'containerSampleChangerLocation': '1', 'proteinAcronym': 'Mnth', 'cellGamma': 0.0, 'cellAlpha': 0.0, 'sampleId': 444185, 'cellBeta': 0.0, 'crystalSpaceGroup': 'R32', 'sampleLocation': '8', 'sampleName': 'sample-E08', 'cellA': 0.0, 'diffractionPlan': (diffractionPlanWS3VO){
diffractionPlanId = 266047
experimentKind = "Default"
exposureTime = 0.0
}, 'cellC': 0.0, 'cellB': 0.0, 'experimentType': 'Default'}, {'holderLength': 22.0, 'code': None, 'containerSampleChangerLocation': '1', 'proteinAcronym': 'Mnth', 'cellGamma': 0.0, 'cellAlpha': 0.0, 'sampleId': 444186, 'cellBeta': 0.0, 'crystalSpaceGroup': 'R32', 'sampleLocation': '9', 'sampleName': 'sample-E09', 'cellA': 0.0, 'diffractionPlan': (diffractionPlanWS3VO){
diffractionPlanId = 266048
experimentKind = "Default"
exposureTime = 0.0
}, 'cellC': 0.0, 'cellB': 0.0, 'experimentType': 'Default'}, {'holderLength': 22.0, 'code': None, 'containerSampleChangerLocation': '1', 'proteinAcronym': 'Mnth', 'cellGamma': 0.0, 'cellAlpha': 0.0, 'sampleId': 444187, 'cellBeta': 0.0, 'crystalSpaceGroup': 'R32', 'sampleLocation': '10', 'sampleName': 'sample-E10', 'cellA': 0.0, 'diffractionPlan': (diffractionPlanWS3VO){
diffractionPlanId = 266049
experimentKind = "Default"
exposureTime = 0.0
}, 'cellC': 0.0, 'cellB': 0.0, 'experimentType': 'Default'}]}"""

@route("/")
def main():
   return static_file("samples_test.html", os.path.dirname(__file__))

@route("/<url:path>")
def serve_static_file(url):
   return static_file(url, os.path.dirname(__file__))

@post('/samples')
def return_samples():
    return samples_info

if __name__ == '__main__':
    run(host="", port="8080",server=GeventServer)
