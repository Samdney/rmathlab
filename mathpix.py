#!/usr/bin/python3

import os
import time
import json
import requests



def downloadFileFromMathpix(headers, baseUrl, pdf_id, fileFormat, outputPath):
	url = f"{baseUrl}/pdf/{pdf_id}.{fileFormat}"
	
	try:
		response = requests.get(url, headers=headers)
		#print(response)
		with open(outputPath, 'wb') as outputFile:
		    outputFile.write(response.content)
		
		if fileFormat == "tex":
			name = os.path.splitext(outputPath)[0]
			print(f"File downloaded to directory {name}")
		else:
			print(f"File downloaded to {outputPath}")
	except:
		print(f"Couldn't download {fileFormat} data from Mathpix")
		
		

def waitForMathpix(headers, baseUrl, pdf_id):
	url = f"{baseUrl}/pdf/{pdf_id}"
	#print(url)

	try:
		while True:
			response = requests.get(url, headers=headers)
			data = response.json()
			#print(data)
			
			status = data.get('status', None)
			#print(status)
			
			if status == "completed":
				print("Waiting for Mathpix completed")
				return True
			elif status == "error":
				print("Error: Mathpix didn't work")
				return False
			else:
				print(f"Status: {status}, waiting for Mathpix")
				time.sleep(5)
	except:
		print("Unexpected error with Mathpix")
		


def sendFileToMathpix(headers, baseUrl, file):
	url = f"{baseUrl}/pdf"
	files = { "file": file }
	
	options = {
            "options_json": json.dumps({
        		"math_inline_delimiters": ["$", "$"],
        		"rm_spaces": True
      		})
   	}
	
	response = requests.post(url, headers=headers, files=files, data=options)
	data = response.json()
	#print(data)
	file.close()
	
	try:
		pdf_id = data["pdf_id"]
		#print("pdf_id: ", pdf_id)
		return pdf_id
	except:
		print("Error: Couldn't send file to Mathpix")
		
		
		
def getFile(pdffilename):
	try:
		file = open(pdffilename, "rb")
		return file
	except IOError:
		print("Can't read file")


