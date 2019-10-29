"""
wcp

From: Hackaday
Oct 22, 2019
rigol-query.py

THIS WORKS!!!!

"""

import visa
resources = visa.ResourceManager('@py')
print(resources.list_resources())

#oscilloscope = resources.open_resource('USB0::6833::1416::DS1EB124907269\x00::0::INSTR')
#Return the Rigol's ID string to tell us it's there
#print(oscilloscope.query('*IDN?'))