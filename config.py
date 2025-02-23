#!/usr/bin/python3

import os
import re
import time
import configparser


def createConfigFile(appdir, configfilename):
	SSH_NAME	= input("Enter your Remakable tablet SSH_NAME:\n")
	APP_ID		= input("Enter your Mathpix APP_ID:\n")
	APP_KEY		= input("Enter your Mathpix APP_KEY:\n")
	
	configfile = f"{appdir}/{configfilename}"
	
	if not os.path.isdir(appdir):
		os.makedirs(appdir, exist_ok=True)		
	
	config = open(configfile, 'w')
	
	config.write("[ssh]\n")
	config.write(f"SSH_NAME\t= {SSH_NAME}\n")
	config.write("\n")
	config.write("[mathpix]\n")
	config.write(f"APP_ID\t\t= {APP_ID}\n")
	config.write(f"APP_KEY\t\t= {APP_KEY}\n")
	
	config.close()

	return True


def readConfig(appdir, configfilename):
	config = configparser.ConfigParser()
	configfile = f"{appdir}/{configfilename}"
	
	try:
	
		created = False
		if not os.path.isfile(configfile):
			print(f"No configfile {configfile} can be found")
			
			dec = input(f"Do you want to create one in {appdir}? yes/no?\n")
			if dec == "yes":
				created = createConfigFile(appdir, configfilename)
				print(f"Configfile {configfile} created")
			else:
				raise
		else:
			created = True
	
		if created:
			config.read(configfile)
		
			SSH_NAME = config["ssh"]["SSH_NAME"]
		
			APP_ID 	= config["mathpix"]["APP_ID"]
			APP_KEY = config["mathpix"]["APP_KEY"]
					
			return { "SSH_NAME": SSH_NAME, "APP_ID": APP_ID, "APP_KEY": APP_KEY }
	
	except KeyError as key:
		key = re.sub(r'[\']', '', str(key))
		
		if key == "mathpix" or key == "ssh":
			print(f"No [{key}] config section in {configfilename}")
		else:
			print(f"No {key} config in {configfilename}")
		
	except:
		raise


