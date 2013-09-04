#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'resources', 'lib'))


import xbmcplugin
import xbmcgui
import xml.etree.ElementTree as ET
import urllib
import urlparse

STATIONS_FILE = os.path.join(os.path.dirname(__file__), 'resources', 'stations.xml')

# Plain Old Python Object for Radio sations
class RadioStation(object):
    name = None
    languages = []
    stream = None

def parse_xml():
    tree = ET.parse(STATIONS_FILE)
    root = tree.getroot()

    # The list of stations we want to create
    stations = []

    for stationE in root.iter('station'):
        station = RadioStation()
        station.name = stationE.find('name').text
        station.languages = stationE.find('lang').text.split()
        station.stream = stationE.find('stream').text
        stations.append(station)

    # Sort in place
    stations.sort(key=lambda x: x.name)

    return stations

def add_stations(stations):
    for station in stations:
        list_item = xbmcgui.ListItem(label=station.name, iconImage='DefaultMusic.png',
                                     thumbnailImage='DefaultMusic.png')
        list_item.setInfo(type='Music', infoLabels={'title': station.name})
        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), 
            url=sys.argv[0] + '?link=' + urllib.quote_plus(station.stream) +\
            '&title=' + station.name +\
            '&mode=2', 
            listitem=list_item)

    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def get_params(query):
    ori = urlparse.parse_qs(query)
    # Convert {'bidule': ['chose']} to {'bidule': 'chose'}
    one_value_per_key_dict = {}
    for o in ori:
        one_value_per_key_dict[o] = ori[o][0]
    return one_value_per_key_dict

params = get_params(sys.argv[2][1:])
mode = params['mode'] if 'mode' in params else 1

if mode=='2': # Play media
    li = xbmcgui.ListItem(label=params['title'], 
        #iconImage=params['thumbnail_url'], 
        #thumbnailImage=params['thumbnail_url'], 
        path=params['link'])
    li.setInfo(type='Music', infoLabels= {'title': params['title']})
    xbmc.Player().play(item=params['link'], listitem=li)
else: # List videos or categories
    add_stations(parse_xml())
