"""Platform for sensor integration."""
from __future__ import annotations

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import (
    DEVICE_CLASS_POWER,
    DEVICE_CLASS_ENERGY,

)
from homeassistant.const import UnitOfTemperature
from homeassistant.const import UnitOfPower, UnitOfEnergy
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.helpers.entity import Entity
from datetime import timedelta
import time
import requests
import random
import logging
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from homeassistant.components.sensor import (PLATFORM_SCHEMA)
from homeassistant.helpers.entity import generate_entity_id


# Validation of the user's configuration
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required('key_ip'): cv.string,
    vol.Required('key_ssid'): cv.string
#    vol.Optional(CONF_PASSWORD): cv.string,
})


_LOGGER = logging.getLogger(__name__)
 
SCAN_INTERVAL = timedelta(seconds=15)  # Interval aktualizácie

_CACHED_VALUES = None

INT16_MAX = 0x7FFF



def to_signed(val):
    if val > INT16_MAX:
        val -= 2**16
    return val

    
def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None
) -> None:
    """Set up the sensor platform."""
    global _USBURL
    global _USBKEY

    _USBURL = 'http://'+config['key_ip']
    _USBKEY = config['key_ssid']
    
    
    add_entities([
        SolaxUsbkey('vyroba', 'výroba', UnitOfPower.WATT, SensorDeviceClass.POWER, SensorStateClass.MEASUREMENT ),
        SolaxUsbkey('grid', 'prebytky do siete', UnitOfPower.WATT,  SensorDeviceClass.POWER , SensorStateClass.MEASUREMENT),
        SolaxUsbkey('dom_spotreba', 'spotreba domu', UnitOfPower.WATT,  SensorDeviceClass.POWER, SensorStateClass.MEASUREMENT ),
        SolaxUsbkey('vyroba_dnes', 'dnešná výroba', UnitOfEnergy.KILO_WATT_HOUR,  SensorDeviceClass.ENERGY, SensorStateClass.TOTAL_INCREASING ),
        SolaxUsbkey('vyroba_celkom', 'celková výroba', UnitOfEnergy.KILO_WATT_HOUR,  SensorDeviceClass.ENERGY, SensorStateClass.TOTAL),
        SolaxUsbkey('celkovo_odovzdana_do_siete', 'celkovo dovzdané do siete', UnitOfEnergy.KILO_WATT_HOUR,  SensorDeviceClass.ENERGY, SensorStateClass.TOTAL),
        SolaxUsbkey('celkovo_spotrebovana', 'celkovo spotrebovaná', UnitOfEnergy.KILO_WATT_HOUR ,  SensorDeviceClass.ENERGY , SensorStateClass.TOTAL)
    ])
    


class SolaxUsbkey(SensorEntity):
    """Representation of a Sensor."""

#    _attr_name = "Solax USB key"
#    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
#    _attr_device_class = SensorDeviceClass.TEMPERATURE
#    _attr_state_class = SensorStateClass.MEASUREMENT

    data_name=''

    def __init__(self, name, display_name, unit_of_measurement, sensor_device_class, state_class):
    
        #self.entity_id = generate_entity_id("sensor.{}", "solaxusbkey_"+name, current_ids=None, hass=self.hass)
        self.entity_id = "sensor.solax_"+name
        self.data_name=name
        self._name = "solax_"+name
        
        self._state = None
        self._attr_name = display_name
        #self._attr_unique_id = "solax_" + name
        self._attr_unique_id = "solax_" + name
        
        self._attr_native_unit_of_measurement = unit_of_measurement
        self._attr_device_class = sensor_device_class
        self._attr_state_class = state_class
        
        if display_name is not None:
            self.display_name = display_name

        self.update()

#    def name(self):
#        return "Solax USB key"
#    @property
#    def state(self):
#        return self._state
    """    
    @property
    def device_state_attributes(self):
        return {
            "vyroba": self._vyroba, 
            "grid": self._grid, 
            "dom_spotreba": self._dom_spotreba, 
            "vyroba_dnes": self._vyroba_dnes, 
            "vyroba_celkom": self._vyroba_celkom, 
            "celkovo_odovzdana_do_siete": self._celkovo_odovzdana_do_siete, 
            "celkovo_spotrebovana": self._celkovo_spotrebovana
            }
    """
    @property
    def should_poll(self):
        return True  # Aktivuje metódu `update` na pravidelné aktualizácie        

    def update(self) -> None:
        global _CACHED_VALUES
        global _USBURL
        global _USBKEY
        if _CACHED_VALUES is None or (time.time()  - _CACHED_VALUES['timestamp']) > SCAN_INTERVAL.total_seconds():
            url = _USBURL
            try:
                response = requests.post(url, data="optType=ReadRealTimeData&pwd="+_USBKEY, timeout=3)
                data=response.json()['Data']
                _CACHED_VALUES = {
                    "vyroba": data[6]+data[7]+data[8], 
                    "grid": to_signed(data[74]), 
                    "dom_spotreba": (data[6]+data[7]+data[8]) - (to_signed(data[74])) ,  #vyroba - grid
                    "vyroba_dnes": data[21] /10, 
                    "vyroba_celkom": ( data[20] * 65535 + data[19]) /10, 
                    "celkovo_odovzdana_do_siete": data[76]/100, 
                    "celkovo_spotrebovana": data[78]/100,
                    "timestamp": time.time()
                    }
                #_LOGGER.error(f"citam z usb kluca" + str(_CACHED_VALUES.get(self.data_name)) + self.data_name + str(data) )
                """                
                self._vyroba = data[6]+data[7]+data[8]
                self._grid = to_signed(data[74])
                self._vyroba_celkom = ( data[20] * 65535 + data[19]) /10
                self._vyroba_dnes = data[21] /10
                self._celkovo_odovzdana_do_siete = data[76]/100
                self._celkovo_spotrebovana=data[78]/100
                """                
            except Exception as e:
                _LOGGER.error(f"Error updating sensor: {e}")
                self._attr_native_value = None
        if _CACHED_VALUES is not None:
            self._attr_native_value = _CACHED_VALUES.get(self.data_name)
        else:
            self._attr_native_value = None


        #self._attr_native_value = random.randint(10,35)

    def update_interval(self):
        return SCAN_INTERVAL        

