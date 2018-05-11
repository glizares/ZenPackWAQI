import json
import urllib

from twisted.internet.defer import inlineCallbacks, returnValue
from twisted.web.client import getPage

from Products.DataCollector.plugins.CollectorPlugin import PythonPlugin

class Locations(PythonPlugin):

    relname='waqiStations'
    modname='ZenPacks.cascadeo.Waqi.WaqiStation'

    requiredProperties= (
        'zWaqiToken',
        'zWaqiLocations'
    )

    deviceProperties=PythonPlugin.deviceProperties+requiredProperties

    @inlineCallbacks
    def collect(self,device,log):
        apiKey=getattr(device,'zWaqiToken',None)
        if not apiKey:
            log.error("API KEY NOT SET")
            log.info("API KEY NOT SET")
            returnValue(None)

        locations=getattr(device,'zWaqiLocations',None)
        if not locations:
            log.error("NO LOCATIONS")
            log.info("NO LCOATIONS")
            returnValue(None)

        rm = self.relMap()

        for location in locations:
            try:
                response = yield getPage('https://api.waqi.info/search/?token={token}&keyword={keyword}'.format(token=apiKey, keyword=urllib.quote(location)))
                response = json.loads(response)
            except:
                returnValue(None)

        if response['status']!='ok':
            log.error("%s: %s", device.id, "Response status is not ok")
            log.info("RESPONSE NOT OK")
            returnValue(None)
        log.info(response)     
        for data in response['data']:
            objMap = self.objectMap({
                 'id': self.prepId(data['uid']),
                 'title': data['station']['name'],
                 'url': data['station']['url']
            })
            log.info(data['uid'])
            log.info(data['station']['name'])
            log.info(data['station']['url'])                 
            rm.append(objMap)
        log.info(rm)
        returnValue(rm)

    def process(self,device,results,log):
        return results

