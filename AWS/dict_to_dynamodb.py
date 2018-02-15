import datetime

def dict_to_item(raw):
	if type(raw) is dict:
		resp = {}
		for k, v in raw.items():
			if v is None:
				resp[k] = {
					'NULL': True
				}
			elif type(v) is str:
				resp[k] = {
					'S': v
				}
			elif isinstance(v, datetime.datetime):
				resp[k] = {
					'S': v.strftime('%d-%m-%Y %H:%M:%S %Z')
				}
			elif type(v) is bool:
				resp[k] = {
					'BOOL': bool(v)
				}
			elif type(v) is int:
				resp[k] = {
					'I': str(v)
				}
			elif type(v) is dict:
				resp[k] = {
					'M': dict_to_item(v)
				}
			elif type(v) is list:
				resp[k] = []
				for i in v:
					resp[k].append(dict_to_item(i))

		return resp
	elif type(raw) is str:
		return {
			'S': raw
		}
	elif type(raw) is int:
		return {
			'I': str(raw)
		}
test = {
	"string": "Hello World!",
	"int": 123,
	"boolean": True,
	"datetime": datetime.datetime.now(),
	"list": ["a", "b"],
	"dict": {
		"item1": "one",
		"item2": "two",
	},
	"none": None,
}
print(dict_to_item(test))