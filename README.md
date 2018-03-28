# ZenPackWAQI

## About
This ZenPack makes use of the World Air Quality Index API from http://aqicn.org/api/ to monitor AQI's of user defined stations.

## Installation Instructions
Run the following command using the ZenPacks.cascadeo.Waqi folder as the `zenoss` user to isntall the ZenPack:
`zenpack --link --install=ZenPacks.cascadeo.Waqi`
`serviced service restart Zenoss.core`

Register for an API key at http://aqicn.org/api/ and use it in the zWaqiToken configuration property.
Add locations or station names to the zWaqiLocations configuration property.
Remodel the device.
