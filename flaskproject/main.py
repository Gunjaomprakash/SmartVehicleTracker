from flask import Flask, request , render_template
import requests
from twilio.twiml.messaging_response import MessagingResponse
from math import radians, cos, sin, asin, sqrt
import itertools
from twilio.rest import Client
f = open("none.txt", "r")
api = f.readline()
def Distance(lat1,lon1, lat2, lon2):
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    lat1 = radians(lat1)
    lat2 = radians(lat2)
      
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
 
    c = 2 * asin(sqrt(a))
    
    # Radius of earth in kilometers. Use 3956 for miles
    r = 6371
      
    # calculate the result
    return(c * r)
def SendReminder(i ,n ,r ):
    account_sid = 'AC23626e6518c1fee7dcf5d40ff4e513b0'
    auth_token = '30e4c13ec4bf267e7cb8ccf7e879f3de'
    client = Client(account_sid, auth_token)
    message = client.messages.create(
                                body='Hello there! '+ r + " is about to reach "+ n + " please be ready!",
                                from_='whatsapp:+14155238886',
                                to=i
                            )
    print(message)
def ro(cnode , dnode, nodename , routename):
    destinationLat = dnode.latitude
    destinationLong = dnode.longitude
    currentLat = cnode.latitude
    currentLong = cnode.longitude
    dis = Distance(currentLat,currentLong,destinationLat,destinationLong)
    print(dis,"km")
    if dis < 5:
        for i in ReminderList[routename][nodename]:
            SendReminder(i , nodename , routename)
class route:
    def __init__(self, stops , currentposition):
        self.stops = list(stops.keys())
        self.currentposition = currentposition
    def StarttoEnd(self):
        pass
class node:
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude
    def loc(self):
        return [self.latitude , self.longitude]
r1currentnode = node(17.595031, 78.452215)
r2currentnode = node(17.595031, 78.452215)
gandimaisamma = node(17.592694,78.407607)
srnagar = node(17.438047, 78.443162)
ameerpet = node(17.434850, 78.444881)
mythrivanam = node(17.436828, 78.443650)
jubileehills = node(17.428375, 78.417405)
r1stops = {"gandimaisamma": gandimaisamma ,  "srnagar" : srnagar,   "ameerpet" : ameerpet}
r2stops = { "mythrivanam" : mythrivanam  , "jubileehills" : jubileehills, "ameerpet" : ameerpet}
route1 = route(r1stops , r1currentnode.loc)
route2 = route(r2stops , r2currentnode.loc)

ReminderList={
    "route1" : {"gandimaisamma": [],  "srnagar" : [],   "ameerpet" : []},
    "route2" : {"mythrivanam" : []  , "jubileehills" : [], "ameerpet" : []}
}
Helpmessage = """Typing Code -- It's Description

Replace {-} as assisted

Route { Bus number } Stops -- To get the stops of that Bus
Route { Bus number } current location -- To get the present location of that Bus
Route { Bus number } current position -- To get the present location of that Bus
Route { Bus number } Remainder { Stop name } -- To get a remainder when the Bus reaches the range of 500m of { Stop name }

Example : Route 1 Stops"""
UpdateStatement = 'Updated Route {} latitude = {} and longitude = {}'
app = Flask(__name__)
@app.route('/updateroute', methods=["POST","GET"])
def update():
    RouteNumber = int(request.args.get('routenumber'))
    uplatitude = float(request.args.get('latitude'))
    uplongitude = float(request.args.get('longitude'))
    if RouteNumber == 1:
        routey = route1
        r1currentnode.latitude = uplatitude
        r1currentnode.longitude = uplongitude
        for i in r1stops:
            ro(r1currentnode , r1stops[i] , i , "Route1")
    if RouteNumber == 2:
        r2currentnode.latitude = uplatitude
        r2currentnode.longitude = uplongitude
        routey = route2
        for j in r2stops:
            ro(r2currentnode , r2stops[j] , j , "Route2")
    return UpdateStatement.format(RouteNumber,routey.currentposition()[0],routey.currentposition()[1])
    
@app.route('/bot', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '').lower()
    user = request.values.get('From')
    resp = MessagingResponse()
    msg = resp.message()
    responded = False
    a = incoming_msg.split(" ")
    if a[0] == 'route':
        strfind = a[0]+a[1]
        rfind=globals()[a[0]+a[1]]
        if "current location" in incoming_msg or "current position" in incoming_msg:
            lat = str(rfind.currentposition()[0])
            lon = str(rfind.currentposition()[1])
            msg.body('https://www.google.co.in/maps/place/'+lat+',+'+lon+'/@'+lat+','+lon+',18z')
            responded = True
        if "stops" in incoming_msg:
            msg.body(" >> ".join(list(rfind.stops)))
            responded = True
        
        if "reminder" in incoming_msg:
            location = a[3]
            if location in rfind.stops:
                ReminderList[strfind][location].append(user)
                print(ReminderList)
                print(user)
                msg.body(user)
                responded = True
        if not responded:
            msg.body('Try sending "help" for the actions that can be performed')
        return str(resp)
    elif "help" == incoming_msg:
            msg.body(Helpmessage)
            responded = True
            return str(resp)
    else:
        msg.body('Try sending "help" for the actions that can be performed')
        return str(resp)
print(r1currentnode.latitude,r1currentnode.longitude)

            
@app.route("/")
def index():
    datafrompythonpush = {
    'api' : api,
    'route1lat' : str(r1currentnode.latitude),
    'route1long' : "+"+str(r1currentnode.longitude),
    'route2lat' : str(r2currentnode.latitude),
    'route2long' : "+"+str(r2currentnode.longitude)}
    return render_template('home2.html', datafrompython = datafrompythonpush)

if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0",port="6900")

