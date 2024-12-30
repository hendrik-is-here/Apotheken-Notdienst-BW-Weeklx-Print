#! /usr/bin/env python
import requests

url_string = 'https://notdienst.sberg.net/api/apipub/notdienst/xmlschnittstelle/QUENGAQGFkRCQl9HWUwFeHFTUEJAT1xMUAZpY21AVFFFHmd4cXBudWx7QENNV0FdQGVTRVgIEAxXV05YUVBedVxMTFBHYExbf0VeDRJIR0FGQVNKVF5jXRoWVElRXQkDHxYHEAwaBBoMChYfAQcDGA0eSVdeQBwFGxIJFgwVBQoaCg4fDBITHBBJWVxZUFhcUXRFfkJJWlEXBQcGHQhXQFJOaUFLVU9XTlQU'

with open('lak.xml', 'wb') as f:
	resp = requests.get(url_string, verify=False)
	f.write(resp.content)
