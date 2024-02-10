#!/usr/bin/env python

import sys, uuid
from oslo_serialization import base64
 
def _encode_name(name):
	uuid_str = name.replace("-", "")
	vol_uuid = uuid.UUID('urn:uuid:%s' % uuid_str)
	vol_encoded = base64.encode_as_text(vol_uuid.bytes)
	
	# 3par doesn't allow +, nor /
	vol_encoded = vol_encoded.replace('+', '.')
	vol_encoded = vol_encoded.replace('/', '-')
	# strip off the == as 3par doesn't like those.
	vol_encoded = vol_encoded.replace('=', '')
	return vol_encoded
 
if len(sys.argv) < 2:
	print("No volume_id(s) supplied")
	sys.exit()
else:
	for volume_id in sys.argv[1:]:
		print("volume_id: " + volume_id + 
              " 3par_id: osv-" + _encode_name(volume_id))

# vim: ts=4
