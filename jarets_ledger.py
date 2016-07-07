import os, json, datetime

class LedgerManager():
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
			lm = jarets_ledger.LedgerManager(config={'LEDGER_FILE': '/path/to/file.json', 'LEDGER_HISTORY': int})
				LEDGER_HISTORY: entries older then x days old will be removed. a value of 0 will never
				remove old values.
		Write any values to your ledger:
			lm.runLedger['key_name'] = 'some value'
		When complete, write out to your file:
			lm.write_ledger_to_file()
	'''
	
	def __init__(self, config):
		# Configs
		self.__ledger_file = config['LEDGER_FILE']
		self.__ledger_history = config['LEDGER_HISTORY']		
		
		# Ledger
		self.runLedger = {}
		self.__fullLedger = {}
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
			error_msg = "Datetime variable was not int: %s" % e
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

	def _set_ledger_dict_key(self):
		if not os.path.isfile(self.__ledger_file):
			self.write_ledger_to_file()

		self.__fullLedger = self._get_ledger_from_file(self.__ledger_file)

		if self.__parentKey not in self.__fullLedger:
			self.__fullLedger[self.__parentKey] = {}
		
		if self.__ledger_history != 0:
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
		return True

	def purge_old_ledger_keys(self):
		oldunixdate = self.set_unix_time(precise=False, daysback=self.__ledger_history)
		for key in self.__fullLedger:
			if int(key) < oldunixdate:
				del self.__fullLedger[key]
		return True