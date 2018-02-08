#!/usr/bin/env python

"""
	@Author		Jaret Deprin

	@Info
		Grains collection for AWS EC2 instances.  No IAM or Instance role is required.
"""

import requests
import json

def get_metadata():
	meta = {
		'InstanceId': False,
		'AccountId': False,
		'Region': False,
		'FetchError': 0
	}
	try:
		r = requests.get('http://169.254.169.254/latest/dynamic/instance-identity/document')
		if r.status_code == 200:
			iid = json.loads(r.text)
			meta['InstanceId'] = iid['instanceId']
			meta['AccountId'] = iid['accountId']
			meta['Region'] = iid['region']
	except:
		meta['FetchError'] = 1
	return {'aws_metadata': meta}
