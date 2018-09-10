import flask
import argparse
import requests
import json
import os
import googlemaps
import dialogflow_v2

app=flask.Flask(__name__)

url="https://www.googleapis.com/geolocation/v1/geolocate?key=AIzaSyDpUu4Ks4VMyW02wV_rp2sWS2jFlzAM09M"

@app.route('/webhook',methods=['POST'])
def webhook():
  req = flask.request.get_json()
  res = processReq(req)
  res = json.dumps(res,indent = 4)
  r=flask.make_response(res)
  r.headers['Context-Type'] = 'application/json'
  print (r)
  return r

def processRequest(req):
  result = req.get("result")
  if result.get("action")== "AskLocation.AskLocation-yes":
    loc=getLocation()
  print(loc)
  speech = loc
  return {
    "speech": speech,
    "displayText": speech,
    "source":"Zomato top restaurants"
  }
def getLocation(app):
  const loc = app.SupportedPermissions.DEVICE_PRECISE_LOCATION
  app.askForPermissions('',[loc])
  return


if __name__ == 'main':
  port = os.getenv('PORT',5000)
  print("starting app %d" % port)
  app.run(debug=Flase,port=port, host='0.0.0.0')
