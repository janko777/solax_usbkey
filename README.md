# solax wifi usbkey component for Home Assistant
read json data from usb wifi key
example POST request, pwd = usb wifi SSID
```
curl -d "optType=ReadRealTimeData&pwd=S?????????" -X POST http://192.168.xx.xx
{"sn":"SX???????","ver":"3.003.02","type":7,"Data":[2358,2343,2349,28,28,29,636,621,654,3071,3473,29,36,877,1233,5000,5001,5000,2,27654,1,32,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,8,0,0,0,0,0,8,9000,0,35,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,41,0,65316,65535,39049,9,8147,11,1907,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],"Information":[9.000,7,"MU902THB040009",8,1.30,1.02,1.33,1.02,0.00,1]}
```
Install custom component:
```
ssh root@your_hass
cd /homeassistant/custom_components/
git clone https://github.com/janko777/solax_usbkey.git
```
Add IP and SSID to configuration.yaml
```
sensor:
  - platform: solax_usbkey
    key_ip: "192.168.xx.xx"
    key_ssid: "SX????????"
```
reboot HASS
