#!/usr/bin/python3

import os
import sys
import json
import subprocess
import urllib.request



def splitname(filename):
    name, ext = os.path.splitext(filename) # e.g. ("document", ".pdf")
    return name, ext



def	downloadPdfFromRM(uuid, filename):

	outfile = splitname(filename)[0] + ".pdf"
	
	url = f"http://10.11.99.1/download/{uuid}/placeholder"
	
	try:
		urllib.request.urlretrieve(url, filename=outfile)
		return True
		#exit(0)
	except Exception as e:
		raise(RuntimeError(f"Could not download {url} from reMarkable USB web interface. Make sure that Settings > Storage > USB web interface is enabled"))
		exit(1)



def getUUIDByFilename(rawDirLocal, filename):
	name, ext = splitname(filename)
	metadataFiles = [metafile for metafile in os.listdir(rawDirLocal) if metafile.endswith('.metadata')]

	for file in metadataFiles:
		with open(os.path.join(rawDirLocal, file)) as metafile:
			data = json.load(metafile)
			#print(data["visibleName"])
	
			if name == splitname(data["visibleName"])[0]:
				#print(file)
				return splitname(file)[0]

	return None



def pcRun(args, cmd, exiterror=None, capture=True):
    if args.verbose:
        print(">", subprocess.list2cmdline(cmd)) # print the command

    proc = subprocess.run(cmd, capture_output=capture, encoding="utf-8")
    if proc.returncode != 0 and exiterror is not None:
        print(proc.stderr, end="")
        print("ERROR: " + exiterror)
        exit(1)

    return proc



def downloadMetadata(args, SSH_NAME, rawDirRemote, rawDirLocal):
    try:
    	print(f"Downloading metadata to {rawDirLocal}")
    	pcRun(args, ["rsync", "--info=progress2", "-az", "--delete-excluded", "--include=*.metadata", "--exclude=*", f"{SSH_NAME}:{rawDirRemote}/", f"{rawDirLocal}/"], exiterror="Failed downloading metadata", capture=False) # --delete-excluded deletes files on PC that are no longer on RM
    except:
    	print("Couldn't access necessary metadata")
    	raise

		
