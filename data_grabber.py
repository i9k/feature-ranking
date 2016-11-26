"""
Data Grabber
"""
import pyodbc
import sys
import pandas as pd
import pickle
import time
import os.path

class Data_Grabber(object):

	def __init__(self, pkl_df, howmany_rows="*", db_name="[TEGA].[TT\igork].AO_PopDiff", dsn="TEGA_DB", pwd="PA$$word914"):

		self.db_name = db_name
		self.get_howmany_rows = howmany_rows
		self.pkl_data = pkl_df
		self.auth = "DSN=" + dsn +";" + "PWD=" + pwd
		self.df = pd.DataFrame()

	def grab(self):

		if os.path.exists(self.pkl_data):
			print("pickled data frame already exists")
			with open(self.pkl_data, "rb") as f:
				self.df = pickle.load(f)
			print("loaded data from file {}".format(self.pkl_data))
		else:
			print("preparing to get data from SQL database...")
			conn = pyodbc.connect(self.auth)
			start_time = time.time()

			if self.howmany_rows != "*":
				sql_line = "select top " + str(howmany_rows) + " from " + self.db_name
			else:
				sql_line = "select " + str(howmany_rows) + " from " + self.db_name

			self.df = pd.read_sql(sql_line, conn)
			end_time = time.time()

			print("done. elapsed time: {} minutes".format(round((end_time-start_time)/60,2)))

	def nrows(self):

		print("number of rows in data frame: {}".format(len(self.df.index)))

	def show_variables(self):

		print("data frame contains the following variables:\n")
		for i, v in enumerate(list(self.df)):
			print("[{}]:\t{}".format(i, v))

	def save_locally(self):

		self.df.to_pickle(self.pkl_data)
		print("saved data frame to file {}".format(self.pkl_data))