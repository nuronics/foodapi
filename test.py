import flask
import requests
import json
import os
import googlemaps
'''import dialogflow_v2
from geolocation.main import GoogleMaps
from geolocation.distance_matrix.client import DistanceMatrixApiClient
from googlemaps import exceptions'''

app = flask.Flask(__name__)

url = 'https://developers.zomato.com/api/v2.1/'
apikey='&apikey=c5062d18e16b9bb9d857391bb32bb52f'

@app.route('/webhook', methods=['POST'])
def webhook():
    req = flask.request.get_json()
    res = processRequest(req)
    print("response :")
    res=json.dumps(res, indent=4)
    r = flask.make_response(res)
    r.headers['Content-Type'] = 'application/json'
    print("result r")
    print(r)
    return r


def processRequest(req):
    result = req.get("result")
    #if result.get("action")== "AskLocation.AskLocation-yes":
    #   loc=getLocation()
    parameters = result.get("parameters")
    
    #landm = str(parameters.get("landmark"))
    #u_loc = geolocationn(landm)
    u_type = str(parameters.get("type"))
    u_cuisine = str(parameters.get("cuisines"))
    u_Collections = str(parameters.get("Collections"))
    query = str(parameters.get("item"))
    longi = str(parameters.get("longi"))
    lat = str(parameters.get("lat")[0])
    
    #url to fetch the details of the client location
   # location_url=url+'locations?query='+u_loc+apikey
    #json_data = requests.get(location_url).json()

  #  entity_id=json_data.get('location_suggestions')[0].get('entity_id')
   # entity_type=json_data.get('location_suggestions')[0].get('entity_type')
   # city_id=json_data.get('location_suggestions')[0].get('city_id')
    search_url=url+'search?q='+str(query)+'&lat='+str(lat)+'&lon='+str(longi)+'&radius=3000&sort=real_distance&order=asc&count=5'+apikey

    json_data=requests.get(search_url).json()
    print(search_url)
    
    namedict=[]
    urldict=[]
    resultstr=''
    for x in range(len(json_data.get('restaurants'))):
        namedict.append(json_data.get('restaurants')[x].get('restaurant').get('name'))
        urldict.append(json_data.get('restaurants')[x].get('restaurant').get('order_url'))
        resultstr = makeresult(resultstr,json_data.get('restaurants')[x].get('restaurant').get('name'))

    #speech=str(namedict)+str(urldict)
    dict = {}
    for x in range(len(json_data.get('restaurants'))):
        dict[json_data.get('restaurants')[x].get('restaurant').get('name')] = json_data.get('restaurants')[x].get('restaurant').get('order_url')

    speech="These are the available Best restaurants in your area, which serve8" +query+"\n"+resultstr+"\n Choose one restaurant of your choice."
    print(speech)
    return {
        "speech": speech,
        "displayText": speech,
        "source":"Zomato top restaurants"
    }

'''def geolocationn(u_loc):
    
    if u_loc == '':
        address = "chaipani jubliee hills checkpost Hyderabad"
    else:
        address = u_loc
        print (address)
    google_maps = GoogleMaps(api_key='AIzaSyCfHC9jA07EFo-hTYkHR1szXOvGD4knDTI')
    if googlemaps != None:

        location = google_maps.search(location=address)

    #    print(location.all())

        my_location = location.first()

       

        for administrative_area in my_location.administrative_area:
            print("%s: %s" % (administrative_area.area_type, administrative_area.name))

        print(my_location.formatted_address)

        print(my_location.lat)
        print(my_location.lng)

    return my_location.formatted_address'''


def makeresult(resultstr,appendstr):

    return resultstr+"\n"+str(appendstr)

'''def fetchcuisines(u_loc):
    cusineurl = url+'cusines?'+u_loc+apikey
    json_data = requests.get(cusineurl).json()
    cuisines = json_data.get('cusines')'''

if __name__ == '__main__':
    port = int(os.getenv('PORT',5000))
    print("Starting app %d" % port)
    app.run(debug=True, port=port, host='0.0.0.0')
