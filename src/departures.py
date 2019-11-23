from datetime import datetime
import requests
import json


def get_EFA_from_VVS(station_id, time=datetime.now(), limit=100):
    """
    send HTTP Request to VVS and return a xml string
    """
    if limit == 1: limit = 2
    # parameters needed for EFA
    zocation_server_active = 1
    ls_show_trains_explicit = 1
    stateless = 1
    language = 'de'
    spenc_id = 0
    any_sig_when_perfect_no_other_matches = 1
    # max amount of arrivals to be returned
    limit = limit
    dep_arr = 'departure'
    type_dm = 'any'
    any_obj_filter_dm = 2
    delete_assigned_stops = 1
    name_dm = station_id
    mode = 'direct'
    dm_line_selection_all = 1
    use_realtime = 1
    output_format = 'json'
    coord_output_format = 'WGS84[DD.ddddd]'

    url = 'http://www2.vvs.de/vvs/widget/XML_DM_REQUEST?'
    url += 'zocationServerActive={:d}'.format(zocation_server_active)
    url += '&lsShowTrainsExplicit{:d}'.format(ls_show_trains_explicit)
    url += '&stateless={:d}'.format(stateless)
    url += '&language={}'.format(language)
    url += '&SpEncId={:d}'.format(spenc_id)
    url += '&anySigWhenPerfectNoOtherMatches={:d}'.format(
        any_sig_when_perfect_no_other_matches
    )
    url += '&limit={:d}'.format(limit)
    url += '&depArr={}'.format(dep_arr)
    url += '&type_dm={}'.format(type_dm)
    url += '&anyObjFilter_dm={:d}'.format(any_obj_filter_dm)
    url += '&deleteAssignedStops={:d}'.format(delete_assigned_stops)
    url += '&name_dm={}'.format(name_dm)
    url += '&mode={}'.format(mode)
    url += '&dmLineSelectionAll={:d}'.format(dm_line_selection_all)

    url += ('&itdDateYear={0:%Y}&itdDateMonth={0:%m}&itdDateDay={0:%d}' +
            '&itdTimeHour={0:%H}&itdTimeMinute={0:%M}').format(time)

    url += '&useRealtime={:d}'.format(use_realtime)
    url += '&outputFormat={}'.format(output_format)
    url += '&coordOutputFormat={}'.format(coord_output_format)

    r = requests.get(url)
    r.encoding = 'UTF-8'
    efa = r.json()
    return efa


def parse_efa(efa, limit_to_one=False):
    parsedDepartures = []
    if not efa or "departureList" not in efa or not efa["departureList"]:
        return parsedDepartures

    for departure in efa["departureList"]:
        stopName = departure["stopName"]
        latlon = departure['y'] + "," + departure['x']
        number = departure["servingLine"]["number"]
        direction = departure["servingLine"]["direction"]
        platform = departure["platform"]

        if "realDateTime" in departure:
            realDateTime = departure["realDateTime"]
        elif "dateTime" in departure:
            realDateTime = departure["dateTime"]
        else:
            realDateTime = None

        if "dateTime" in departure and "realDateTime" in departure:
            dateTimeDatetime = datetime(
                year=int(departure["dateTime"]["year"]),
                month=int(departure["dateTime"]["month"]),
                day=int(departure["dateTime"]["day"]),
                hour=int(departure["dateTime"]["hour"]),
                minute=int(departure["dateTime"]["minute"]),
            )
            realDateTimeDatetime = datetime(
                year=int(departure["realDateTime"]["year"]),
                month=int(departure["realDateTime"]["month"]),
                day=int(departure["realDateTime"]["day"]),
                hour=int(departure["realDateTime"]["hour"]),
                minute=int(departure["realDateTime"]["minute"]),
            )
            timeDelta = realDateTimeDatetime - dateTimeDatetime
            delay = int(timeDelta.total_seconds()/60)
        else:
            delay = 0

        departureObject = {
            "stopName": stopName,
            "number": number,
            "direction": direction,
            "platform": platform,
            "departureTime": realDateTime,
            "delay": delay,
            "stationCoordinates": latlon
        }

        parsedDepartures.append(departureObject)
    if limit_to_one: return json.dumps(parsedDepartures[0])
    return parsedDepartures


def departures(station_id, time=datetime.now(), limit=100):
    if limit == 1: return parse_efa(get_EFA_from_VVS(station_id, time=time, limit=limit), limit_to_one=True)
    return parse_efa(get_EFA_from_VVS(station_id, time=time, limit=limit))
