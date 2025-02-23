#!/usr/bin/python3

import os
import zipfile
import argparse
from pathlib import Path


from config import *
from remarkable import *
from mathpix import *



# Path of the Python script (Directory of this file)
DIR = os.path.dirname(os.path.abspath(__file__))
#print("1: ", DIR)

# Path from which you execute the Python script (The current working directory)
CURWORK_DIR = os.getcwd()
#print("2: ", CURWORK_DIR)




APP_NAME 		= "rmathlab"

HOME_DIR 		= Path.home()
APP_DIR 		= f"{HOME_DIR}/.{APP_NAME}"
RM_DIR_REMOTE 	= "/home/root/.local/share/remarkable/xochitl"
METADATA_SUBDIR	= "tmp_metadata"
BASE_URL		= "https://api.mathpix.com/v3"	# "https://api.mathpix.com/v3/pdf"




parser = argparse.ArgumentParser(
	prog = f"{APP_NAME}", description = "Send file from your Remarkable tablet to Mathpix and receive tex, mmd, docx, html, lines.json, lines.mmd.json (default: tex)",
	)
parser.add_argument(
	"filename", type=str, default="", help="The name of the file you want to send to Mathpix (mandatory argument)"
	)
parser.add_argument(
	"-l", "--local", action="store_true", help="Pick local file. Don't fetch from the Remarkable tablet."
	)
parser.add_argument(
	"-f", "--fileformat", type=str, default="tex", help="Output file format: tex, mmd, docx, html, lines.json, lines.mmd.json (default: tex)"
	)
parser.add_argument(
	"-out", "--outputfilename", type=str, default="", help="The name of the output file (default: same like filename)"
	)
parser.add_argument(
	"-cdir", "--appdir", type=str, default=f"{APP_DIR}", help=f"Path of the app directory. Containing the config file and temporary data. (default: {APP_DIR})"
	)
parser.add_argument(
	"-c", "--configfile", type=str, default="config.ini", help="Name of your configfile in your rm-mathrec directory (default: config.ini)"
	)
parser.add_argument(
	"-v", "--verbose", action="store_true", help="Print executed shell commands"
	)
	
#parser.add_argument("name", type=str, nargs="?", default="remarkable", help="SSH hostname of reMarkable reachable with \"ssh [name]\" without password (default: remarkable)") # TODO



if __name__ == "__main__":
		
	"""
	# Read configs
	"""
	args			= parser.parse_args()
	filename		= getattr(args, "filename")
	outputfilename	= getattr(args, "outputfilename")
	appdir			= getattr(args, "appdir")
	configfilename	= getattr(args, "configfile")
	fileFormat		= getattr(args, "fileformat") # tex, mmd, docx, html, lines.json, lines.mmd.json, default: tex

	filename = os.path.splitext(filename)[0]

	if outputfilename == "":
		outputfilename = f"{filename}"

	outputfilename = f"{CURWORK_DIR}/{outputfilename}"

	try:
			
		config = readConfig(appdir, configfilename)
		#print(config)
		
		fileLocal = args.local

		"""
		# Remarkable
		"""
		metadataDirLocal = f"{appdir}/{METADATA_SUBDIR}"
		#metadataDirLocal = os.path.abspath(f"{METADATA_SUBDIR}")
			
		if fileLocal == False:
		
			#checkSSHConnection(config["SSH_NAME"]) # TODO
			
			downloadMetadata(args, config["SSH_NAME"], RM_DIR_REMOTE, metadataDirLocal)
			
			uuid = getUUIDByFilename(metadataDirLocal, f"{filename}")
			if uuid == None:
				print(f"Couldn't find filename: {filename}")
				raise
			#else:
			#	print(uuid)
		
			downloadPdf = downloadPdfFromRM(uuid, f"{CURWORK_DIR}/{filename}")

		"""
		# Mathpix
		"""
		if fileLocal or downloadPdf:
			headers = { "APP_ID": config["APP_ID"], "APP_KEY": config["APP_KEY"] }
			#print(headers)
				
			pdffilename = f"{CURWORK_DIR}/{os.path.splitext(filename)[0]}.pdf"
			file = getFile(pdffilename)
			
			pdf_id = sendFileToMathpix(headers, BASE_URL, file)
						
						
			if fileFormat == "tex":
				outputPath = f"{outputfilename}.zip" # .tex.zip
			else:
				outputPath = f"{outputfilename}.{fileFormat}"
			
		
			if pdf_id and waitForMathpix(headers, BASE_URL, pdf_id):
				downloadFileFromMathpix(headers, BASE_URL, pdf_id, fileFormat, outputPath)


			if fileFormat == "tex":
				with zipfile.ZipFile(outputPath, 'r') as zipRef:
					name = os.path.splitext(outputPath)[0]
					zipRef.extractall(name)
					
				# Remove .zip folder
				os.remove(outputPath)
		
	except:
		print("An unexpected error occured")


