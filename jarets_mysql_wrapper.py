"""
	@Author		Jaret Deprin
	
	@Usage
	import jarets_mysql_wrapper
	# All parameters are required even if user/pass are empty
	c = jarets_mysql_wrapper.Mysql(DBHOST="localhost", DBNAME="test", DBUSER="", DBPASS="")
	
	# Stage query
	c.__stage = True
	Will print queries / values but not execute them.
	
	# Select statment examples
	results = c.select(table, columns, where(optional))
	results = c.select("jdtest", "*")
	results = c.select("jdtest", "id", "name")
	results = c.select("jdtest", "id", "name", where="id=2")
	results = c.select("jdtest", "id", "name", where="state='running' AND bool=True")
	
	# Insert statement examples
	# Both keyword arguments and un-named arguments are supported
	# Use caution with un-named arguments as they could insert valued into incorrect
		fields if you write the values in the incorrect order.
	new_row_primarykey = c.insert(table, **column_names=values)
	new_row_primarykey = c.insert("jdtest", state="stopped", ip="10.1.1.5", name="host5", bool=True)
	new_row_primarykey = c.insert("jdtest", 6,"host6","running",False,"10.1.1.6")
	
	# Update statement examples
	c.update(table, where, **column_names=values)
	c.update("jdtest", where="id=6", ip="10.1.1.6", bool=False)
	
	# Delete statement examples
	c.delete(table, where)
	c.delete("jdtest", where="id=6")
	
"""

import MySQLdb, MySQLdb.cursors

class Mysql(object):
	__instance = None	
	__session = None
	__connection = None
	
	def __init__(self, *args, **kwargs):
		self.__host = kwargs.get('hostname')
		self.__user = kwargs.get('user')
		self.__password = kwargs.get('password')
		self.__database = kwargs.get('database')
		self.__stage = kwargs.get('stage')
	
	def __open(self):
		try:
			conn = MySQLdb.connect(host=self.__host,
								user=self.__user,
								passwd=self.__password,
								db=self.__database,
								cursorclass=MySQLdb.cursors.DictCursor)
			self.__connection = conn
			self.__session = conn.cursor()
		except MySQLdb.Error, e:
			print "MySQL Connection Error [%d]: %s" % (e.args[0], e.args[1])

	def __close(self):
		try:
			self.__session.close()
			self.__connection.close()
		except MySQLdb.Error, e:
			print "MySQL Error Closing [%d]: %s" % (e.args[0], e.args[1])

	def insert(self, table, *args, **kwargs):
		values = None
		query = "INSERT INTO %s" % table		
		if kwargs:
			keys = kwargs.keys()
			values = kwargs.values()
			query += "(" + ",".join(["%s"]*len(keys)) % tuple(keys) + ") VALUES(" + ",".join(["%s"]*len(values)) + ")"
		elif args:
			values = args
			query += " VALUES(" + ",".join(["%s"]*len(values)) + ")"
		if self.__stage is True:
			print query % (values,)
			return True
		self.__open()
		self.__session.execute(query, values)
		self.__connection.commit()
		self.__close()
		return self.__session.lastrowid
			
	def select(self, table, *args, **kwargs):
		result = None
		keys = args
		query = "SELECT " + ",".join(keys) + " FROM " + table
		if kwargs.get('where') is not None:
			query += " WHERE %s" % kwargs['where']
		self.__open()
		self.__session.execute(query)
		self.__connection.commit()
		result = self.__session.fetchall()
		self.__close()
		return result
		
	def update(self, table, where, **kwargs):
		values = None
		values = kwargs.values()
		update_list = ["" + key + "=%s" for key in kwargs.iterkeys()]
		query = "UPDATE " + table + " SET " + ",".join(update_list) + " WHERE " + where
		if self.__stage is True:
			print query % (values,)
			return True
		self.__open()
		self.__session.execute(query, values)
		self.__connection.commit()
		self.__close()
		
	def delete(self, table, where):
		query = "DELETE FROM %s WHERE %s" % (table, where)
		if self.__stage is True:
			print query
			return True
		self.__open()
		self.__session.execute(query)
		self.__connection.commit()
		self.__close()
		
	def call_store_procedure(self, name, *args):
		result_sp = None
		self.__open()
		self.__session.callproc(name, args)
		self.__connection.commit()
		result_sp = self.__session.fetchall()
		self.__close()
		return result_sp
		
	def stage_query(self, query, values)
		
