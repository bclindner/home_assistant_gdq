from homeassistant.helpers.entity import Entity
import urllib.request as request
import re

regex = re.compile("Donation Total:\n\$([0-9\.]+) ")

def getDonationTotal(event):
    """
    Get the current donation total from the GDQ donation tracking website.
    """
    url = "https://gamesdonequick.com/tracker/index/" + event
    req = request.Request(
        url,
        # spoof user agent here; we're not supposed to be scraping this
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36"
        }
    )
    with request.urlopen(req) as response:
        html = response.read().decode('utf-8')
    total = regex.search(html)
    if total:
        return total.group(1)
    else:
        raise Exception("Failed to get GDQ donation total!")

def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the sensor platform."""
    add_devices([GDQSensor()])

class GDQSensor(Entity):
    """The GDQ Sensor class."""

    def __init__(self):
        """Initialize the sensor."""
        self._state = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return 'GDQ Donation Total'

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return '$'

    def update(self):
        """
        Get the donation total and set it in the state.
        """
        self._state = getDonationTotal('sgdq2019')
