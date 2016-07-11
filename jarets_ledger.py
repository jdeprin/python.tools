'''
	@Author		Jaret Deprin
	
	@Info
	Originally created keep a daily record of success / failures during automated
	jobs.  This allows you to tally results over time and pushed results to a
	notification services or through email.
	
	Ledger file is used as a poor mans flat file database
	Ledger file is in json format & converted to a dictionary for writing
	
	Ledger keys are unix timestamps. top level keys are days with a 00:00:00 timestamp
	Children keys are exact times when the script is executed.
	
	@Usage
	Initialize the class:
		import jarets_ledger
		lm = jarets_ledger.LedgerManager(ledger_file='/path/to/file.json', ledger_history=int})
			ledger_history: entries older then x days old will be removed. A value of 0 or if the 
			arguemnt is not defined will never remove old values.
	Write any values to your ledger:
		lm.write("key","value1","value2",['value4','value5']))
	When complete, write out to your file:
		lm.write_ledger_to_file()
'''
	
import os, json, datetime

class LedgerManager(object):
	
	def __init__(self, *args, **kwargs):
		# Configs
		self.__ledger_file = kwargs.get('ledger_file')
		self.__ledger_history = kwargs.get('ledger_history')		
		
		# Ledger
		self.__runLedger = dict()
		self.__fullLedger = dict()
		self.__parentKey = str(self.set_unix_time(precise=False))
		self.__runKey = str(self.set_unix_time(precise=True))
		
		# Prep ledger file
		self._set_ledger_dict_key()
	
	@staticmethod
	def set_unix_time(precise=True, daysback=0):
		if not isinstance(daysback, int):
			raise ValueError('Invalid number of days specified: %s' % daysback)
		try:
			day = datetime.datetime.now() - datetime.timedelta(days=daysback)
		except Exception as e:
			error_msg = "Error creating datetime for dictionary keys: %s" % e
			exit(error_msg)
		if not precise:
			day = datetime.datetime(day.year, day.month, day.day)
		return int(time.mktime(day.timetuple()))
	
	@staticmethod
	def _get_ledger_from_file(ledger):
		try:
			with open(ledger) as data_file:
				leddict = json.load(data_file)
			return leddict
		except IOError as e:
			error_msg = "Ledger file error. Exiting. %s" % e
			exit(error_msg)
		except ValueError as e:
			error_msg = "invalid json: %s" % e
			exit(error_msg)
		except Exception as e:
			error_msg = "Error getting ledger file: %s" % e
			exit(error_msg)

	def _set_ledger_dict_key(self):
		if not os.path.isfile(self.__ledger_file):
			self.write_ledger_to_file()

		self.__fullLedger = self._get_ledger_from_file(self.__ledger_file)

		if self.__parentKey not in self.__fullLedger:
			self.__fullLedger[self.__parentKey] = dict()
		
		if (self.__ledger_history != 0) or (self.__ledger_history is not None):
			self.purge_old_ledger_keys()
		return True

	def write_ledger_to_file(self):
		self.__fullLedger[self.__parentKey][self.__runKey] = self.__runLedger
		try:
			with open(self.__ledger_file, 'w+') as outfile:
				json.dump(self.__fullLedger, outfile)
		except IOError as e:
			error_msg = "Error creating ledger file.  Check folder permissions. Exiting. %s" % e
			exit(error_msg)
		except Exception as e:
			error_msg = "Error writing ledger file: %s" % e
			exit(error_msg)
		return True
	
	def purge_old_ledger_keys(self):
		oldunixdate = set_unix_time(precise=False, daysback=self.ledger_history)
		logging.debug('Purging old entries from ledger file.')
		temp = dict(self.fullLedger)
		for key in self.fullLedger:
			if int(key) < oldunixdate:
				del temp[key]
		self.fullLedger = dict(temp)
		return True

	def write(self, *args):
		key = args[0]
		value = args[1:]
		self.__runLedger[key] = value
		return True
		