# python_tools
Repo for my tools

-----------------------------------------

Feel free to use these at your own risk.


jarets_mysql_wrapper.py
This is a general wrapper for MySQLdb.  pip install MySQLdb-python. Created intially for use in SWARM syncing jobs this provides a nice and clean interface for running general MySQL commands such as SELECT, UPDATE, INSERT, and DELETE.

jarets_ledger.py
A simple flat file database primarily intended to be used to keep track of results for cron jobs running multiple times a day.
I currently use this to keep track of success or failures of the Akamai to S3 log syncing jobs for HMOF and TCK.  Success / failure notifications are sent nightly.
