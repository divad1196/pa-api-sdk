# PaloAlto API: Insight

## Existing tools

### Migration tool

[Expedition](https://live.paloaltonetworks.com/t5/expedition/ct-p/migration_tool) is the 4th version of migration tool and can apparently delete [all unused objects](https://live.paloaltonetworks.com/t5/automation-api-discussions/how-to-quickly-find-and-remove-unused-objects-in-policy/td-p/230055). It is worth trying to use this tool if a cli is available.

### Libraries

* [pan-os-python](https://github.com/PaloAltoNetworks/pan-os-python): Developped by PaloAltoNetworks. The library is maintained but it is really not practical to use. It is subdocumented and strange to use.

  ```python
  from panos.panorama import Panorama
  from panos.objects import AddressObject

  pano = Panorama(hn, un, pw)

  # You need to give the direct parent
  # and explicitly retrieve the data manually
  AddressObject.refreshall(pano)

  # Before being able to use it
  addr = pano.findall(AddressObject)
  ```

  * [How to get all shared address object](https://github.com/PaloAltoNetworks/pan-os-python/issues/427)

  * [Documentation - HowTo](https://github.com/PaloAltoNetworks/pan-os-python/blob/develop/docs/howto.rst)

  * [Code Sample: Ensure security rule](https://github.com/PaloAltoNetworks/pan-os-python/blob/master/examples/ensure_security_rule.py)
- [pan-python](https://github.com/kevinsteves/pan-python/tree/master): wrapper for the XML API. (The [documentation](http://api-lab.paloaltonetworks.com/pan-python.html) seems to be hosted by PaloAltoNetworks)

### Client

* [pan-configurator](https://github.com/cpainchaud/pan-configurator) ?

* [panxapi](https://github.com/kevinsteves/pan-python/blob/master/doc/panxapi.rst) python client for the xml api. It does not do much more.

## Existing APIs

* **REST API**: We access the resources directly.

* **XML API**: We traverse an xml configuration containing all informations using xpath.
  This seems to be the most powerful API

  * [Explore the API](https://docs.paloaltonetworks.com/pan-os/9-1/pan-os-panorama-api/get-started-with-the-pan-os-xml-api/explore-the-api#id32696dff-45b0-40c6-abdf-ef7fbe8a6604): We can explore the API, e.g. through the [browser](https://docs.paloaltonetworks.com/pan-os/9-1/pan-os-panorama-api/get-started-with-the-pan-os-xml-api/explore-the-api/use-the-api-browser#id676e85fa-1823-466a-9e31-269dc6eb433a)

  * [Configuration (API) ](https://docs.paloaltonetworks.com/pan-os/10-1/pan-os-panorama-api/pan-os-xml-api-request-types/configuration-api)

  * [Use XPath to Get Active Configuration](https://docs.paloaltonetworks.com/pan-os/10-1/pan-os-panorama-api/pan-os-xml-api-request-types/configuration-api/get-active-configuration/use-xpath-to-get-active-configuration#:~:text=Use%20action%3Dshow%20with%20no%20additional%20parameters%20to%20retrieve,example%2C%20to%20retrieve%20just%20the%20security%20rulebase%3A%20xpath%3D%2Fconfig%2Fdevices%2Fentry%2Fvsys%2Fentry%2Frulebase%2Fsecurity)

  We can for example find the `entry` referencing an object as a member

  ```python
  /config/devices/entry/device-group//member[text() = 'RAR_ZRH-SNAT_Subnet']//ancestor::entry[position() = 1]
  ```

  Nb: this is usefull to find the dependencies, but it is not easy to delete this entry

### Other informations

* [security policy filtering](https://live.paloaltonetworks.com/t5/blogs/tips-and-tricks-filtering-the-security-policy/ba-p/163250): it is apparently possible to filter the policies according to their members

* [XML API walkthrough](https://blr-pan-01.hq.k.grp/php/rest/browse.php/config%3A%3Adevices%3A%3Aentry%5B%40name%3D%27localhost%252Elocaldomain%27%5D%3A%3Adevice-group)

* [Embedded REST API documentation](https://blr-pan-01.hq.k.grp/restapi-doc/#tag/objects-addresses)
