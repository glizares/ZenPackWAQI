import json
import urllib

from twisted.internet.defer import inlineCallbacks, returnValue
from twisted.web.client import getPage

from Products.DataCollector.plugins.CollectorPlugin import PythonPlugin

class Locations(PythonPlugin)

    relname='WaqiStations'
    modname='ZenPacks.cascadeo.Waqi.WaqiDevice

    requiredProperties= (
        'zWaqiToken',
        'zWaqiLocations'
    )

    deviceProperties=PythonPlugin.deviceProperties+requiredProperties

    @inlineCallbacks
    def collect(self,device,log):
        apiKey=getattr(device,'zWaqiToken',None)
        if not apikey:
            returnValue(None)

        locations=getattr(device,'zWaqiLocations',None)
        if not locations:
            returnValue(None)

        rm = self.relMap()

        for location in locations:
            try:
                response = yield getPage('https://api.waqi.info/search/?token={token}&keyword={keyword]'.format(token=apiKey, keyword=urllib.quote(location))
                response = json.loads(response)
            except:
                returnValue(None)

        if response['status']!='ok':
            log.error("%s: "%s", device.id, "Response status is not ok")
            returnValue(None)
     
        for data in response['data']:
            objMap = self.objectMap({
                 'id':self.prepId(data['uid']),
                 'title': data['station']['name'],
                 'url': data['station']['url']
            })
            rm.append(objMap)

        returnValue(rm)

    def process(self,device,results,log):
        return results

