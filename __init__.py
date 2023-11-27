import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

"""
DOMAIN = "solax_usbkey"

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Required('key_ssid'): cv.string,
        vol.Required('key_ip'): cv.string,
    })
}, extra=vol.ALLOW_EXTRA)
"""

"""
def setup(hass: HomeAssistant, config: ConfigType) -> bool:
    global _USBURL
    global _USBKEY
    
    conf = config[DOMAIN]
    _USBURL = 'http://'+conf['key_ip']
    _USBKEY = conf['key_ssid']
    return True

"""