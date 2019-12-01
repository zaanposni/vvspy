from datetime import datetime, timezone
import requests
import json


def get_EFA_from_VVS(origin, destination, departure):
    url = "https://www3.vvs.de/mngvvs/XML_TRIP_REQUEST2"
    params = {"SpEncId": "0", "calcOneDirection": "1", "changeSpeed": "normal", "computationType": "sequence",
                   "coordOutputFormat": "EPSG:4326", "cycleSpeed": "14", "deleteAssignedStops": "0",
                   "deleteITPTWalk": "0",
                   "descWithElev": "1", "illumTransfer": "on", "imparedOptionsActive": "1", "itOptionsActive": "1",
                   "itdDate": departure.strftime('%Y%m%d'), "itdTime": departure.strftime('%H%M'),
                   "language": "de", "locationServerActive": "1",
                   "macroWebTrip": "true", "name_destination": str(destination), "name_origin": str(origin),
                   "noElevationProfile": "1", "noElevationSummary": "1", "outputFormat": "rapidJSON",
                   "outputOptionsActive": "1", "ptOptionsActive": "1", "routeType": "leasttime",
                   "searchLimitMinutes": "360", "securityOptionsActive": "1", "serverInfo": "1",
                   "showInterchanges": "1",
                   "trITArrMOT": "100", "trITArrMOTvalue": "15", "trITDepMOT": "100", "trITDepMOTvalue": "15",
                   "tryToFindLocalityStops": "1", "type_destination": "any", "type_origin": "any",
                   "useElevationData": "1", "useLocalityMainStop": "0", "useRealtime": "1",
                   "useUT": "1", "version": "10.2.10.139", "w_objPrefAl": "12", "w_regPrefAm": "1"}

    r = requests.get(url, params=params)
    r.encoding = 'UTF-8'
    efa = r.json()
    return efa


def parse_efa(efa, limit=100):
    parsedTrips = []
    if not efa or "journeys" not in efa or not efa["journeys"]:
        return parsedTrips
    for journey in efa["journeys"]:
        connections = []
        for connection in journey["legs"]:
            duration = connection.get("duration", "None")
            origin = connection["origin"].get("name", "None")
            originName = connection["origin"].get("disassembledName", "None")
            originType = connection["origin"].get("pointType", "None")
            departureTimePlanned = datetime.strptime(connection["origin"]["departureTimePlanned"][:-1], '%Y-%m-%dT%H:%M:%S')
            departureTimeEstimated = datetime.strptime(connection["origin"]["departureTimeEstimated"][:-1], '%Y-%m-%dT%H:%M:%S')

            departureDelta = departureTimeEstimated - departureTimePlanned
            departureDelay = int(departureDelta.total_seconds() / 60)

            destination = connection["destination"].get("name", "None")
            destinationName = connection["destination"].get("disassembledName", "None")
            destinationType = connection["destination"].get("pointType", "None")
            arrivalTimePlanned = datetime.strptime(connection["destination"]["arrivalTimePlanned"][:-1], '%Y-%m-%dT%H:%M:%S')
            arrivalTimeEstimated = datetime.strptime(connection["destination"]["arrivalTimeEstimated"][:-1], '%Y-%m-%dT%H:%M:%S')

            arrivalDelta = arrivalTimeEstimated - arrivalTimePlanned
            arrivalDelay = int(arrivalDelta.total_seconds() / 60)

            stoppingPointPlanned = connection["destination"]["properties"].get("stoppingPointPlanned", "None")

            transportation = connection["transportation"].get("name", "None")
            transportationName = connection["transportation"].get("disassembledName", "None")
            transportationNumber = connection["transportation"].get("number", "None")
            transportationDescription = connection["transportation"].get("description", "None")

            connectionObject = {
                "duration": duration,
                "origin": origin,
                "originName": originName,
                "originType": originType,
                "departureTimePlanned": str(departureTimePlanned),
                "departureTimeEstimated": str(departureTimeEstimated),
                "departureDelay": departureDelay,
                "destination": destination,
                "destinationName": destinationName,
                "destinationType": destinationType,
                "arrivalTimePlanned": str(arrivalTimePlanned),
                "arrivalTimeEstimated": str(arrivalTimeEstimated),
                "arrivalDelay": arrivalDelay,
                "stoppingPointPlanned": stoppingPointPlanned,
                "transportation": transportation,
                "transportationName": transportationName,
                "transportationNumber": transportationNumber,
                "transportationDescription": transportationDescription
            }

            connections.append(connectionObject)
        duration = sum([dur["duration"] for dur in connections])
        trip = {
            "duration": duration,
            "connections": connections
        }
        parsedTrips.append(trip)
    return parsedTrips[:int(limit)]


def gettrip(origin, destination, time=0, limit=100):
    if not time: time = datetime.now()
    return parse_efa(get_EFA_from_VVS(origin, destination, departure=time), limit=limit)
