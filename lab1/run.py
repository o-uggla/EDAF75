#!/usr/bin/python3

import sqlite3
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("sql_file")
args = ap.parse_args()

sql_string = ""
with open(args.sql_file, 'r') as f_in:
    sql_string = f_in.read()


conn = sqlite3.connect("lab1.sqlite")
c = conn.cursor()


print(sql_string)
for substring in sql_string.split(";"):
    c.execute(substring)

print("\n".join([str(x) for x in c.fetchall()]))

c.close()
