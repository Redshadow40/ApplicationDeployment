# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
import salt.client
from tableid import table
from download import downloadFile
from runjob import checkInstallFile, checkValidationFile, extractPackage, beginRunJob, checkVersion
from sitesurvey import getSiteSurvey, createSiteTable, saveSiteSurvey
import logging
from multiprocessing import Process
from django.http import JsonResponse
import os
import socket

logger = logging.getLogger(__name__)
POST_KEY = '1'
RUNJOB = None
INSTALL_LOG_FILE = '/var/log/saltInstall/'

def index(request, info=''):
	logger.info(request.body)
	installFileFound = checkInstallFile()
	return render(request, 'index.html', {'filefound': installFileFound, 'info': info})

def installwizard(request):
	return render(request, 'installwizard.html');

def startinstall(request):
	return render(request, 'installcontent/startinstall.html');

def review(request):
	currentVersion = checkVersion()
	return render(request, 'installcontent/review.html', {'currentVersion': currentVersion});

def filemanage(request):
	return render(request, 'filemanage.html');

def finishinstall(request):
	global RUNJOB
	installationStatus = False
	logfilename = None
        if RUNJOB != None and RUNJOB.returnJobType() == "Installation":
                installationStatus = RUNJOB.returnRunStatus()
		logfilename = RUNJOB.getLogFile()
		logfilename = logfilename[logfilename.rfind('/') + 1:]
	installVersion = checkVersion
	return render(request, 'installcontent/finishinstall.html', {'logfilename': logfilename, 'installStatus': installationStatus, 'installVersion': installVersion})

def tableEntityId(request):
	global POST_KEY
	log = ''
	logger.info(request.body)
  	if request.method == 'POST':
		if POST_KEY != request.POST['csrfmiddlewaretoken']:
			if request.POST['ChkApply'] == 'true':
    				log += table.tableApplyID(request)
				if log == '':
					log = 'All tables are currently active'
    			elif request.POST['ChkReset'] == 'true':
				log += table.tableReset(request)
			POST_KEY = request.POST['csrfmiddlewaretoken']   

  	localSalt = salt.client.LocalClient()
  	tables = localSalt.cmd('tc*', 'grains.get', ['entityID'])
	activeJobs = table.checkTableJobs();
  	return render(request, 'tableid.html', {'tables': tables, 'log': log, 'activeJobs': activeJobs})

def sitesurvey(request):
	global POST_KEY
	logger.info(request.body)
	if request.method == 'POST':
		if POST_KEY != request.POST['csrfmiddlewaretoken']:
			saveSiteSurvey(request)
		POST_KEY = request.POST['csrfmiddlewaretoken']
	siteData = getSiteSurvey()
	if not siteData == None:
        	stringData = createSiteTable(siteData)
	else:
		stringData = None
	return render(request, 'installcontent/sitesurvey.html', {'sitesurvey': stringData})

def uploadPP(request):
	if request.method == 'POST' and request.FILES['ppinstallFile']:
		ppFile = request.FILES['ppinstallFile']
		if os.path.isfile(ppFile.name):
			os.remove(ppFile.name)
		if os.path.isfile('uploadedFile.txt'):
			with open('uploadedFile.txt', 'r') as f:
				oldfile = f.read()
			if os.path.isfile(oldfile):
				os.remove(oldfile)
		fs = FileSystemStorage()
		filename = fs.save(ppFile.name, ppFile)
		with open('uploadedFile.txt', 'w') as f:
			f.write(ppFile.name)
		extractPackage(ppFile.name)
	
	currentVersion = None
	installFileFound = checkInstallFile()
	if installFileFound:	
		currentVersion = checkVersion()	

	return render(request, 'installcontent/uploadpp.html', {'currentVersion': currentVersion, 'filefound': installFileFound})

def installPP(request):
	logger.info(request.body)
	installFileFound = checkInstallFile()
	currentVersion = checkVersion()	
	return render(request, 'installcontent/installpp.html', {'currentVersion': currentVersion, 'filefound': installFileFound})

def downloadSiteSurvey(request):
	logger.info(request.body)
    	filePath = '/srv/pillar/sitesurvey.sls'
	return downloadFile(request, filePath, 'sitesurvey.sls')

def showlogfile(request, filename):
	global INSTALL_LOG_FILE
	if not os.path.isfile(INSTALL_LOG_FILE + filename):
		return HttpResponse(filename + ' not found')
	logtext = ''
	with open(INSTALL_LOG_FILE + filename) as f:
		for i , line in enumerate(f):
			logtext += line + '<br>'

	return HttpResponse(logtext)

def downloadlogfile(request, filename):
	global INSTALL_LOG_FILE
	logger.info(request.body)
	filePath = INSTALL_LOG_FILE + filename
	return downloadFile(request, filePath, filename)

def validation(request):
	logger.info(request.body)
	validateFileFound = checkValidationFile()

	return render(request, "validation.html", {'filefound': validateFileFound});

############ API ####################
def installFileFound(request):
	logger.info(request.body)
	installFileFound = checkInstallFile()
	return JsonResponse({'filefound': installFileFound})

def activeValidationPP(request, position=0):
        global RUNJOB
        if RUNJOB == None or RUNJOB.returnJobType() != "Validation":
                return JsonResponse({})
        json = {'activeValidate': []}
        filename = RUNJOB.getTmpLogFile()
        with open(filename, 'r') as f:
                for i, line in enumerate(f):
                        if i >= int(position):
                                json['activeValidate'].append(line.replace('\n', ''))
        return JsonResponse(json)

def beginValidationPP(request):
        logger.info(request.body)
        global RUNJOB
        if RUNJOB == None or not RUNJOB.isAlive():
                RUNJOB = beginRunJob('/srv/salt/validation.sls', 'Validation', keeplogfile=False, forceContinue=True)
                RUNJOB.daemon = True
                RUNJOB.start()
                return JsonResponse({'validate': 'Validation started'})
        return JsonResponse({'validate': RUNJOB.returnJobType() + ' already running'})

def listlogfiles(request):
        logFiles = []
        for (dirpath, dirnames, filenames) in os.walk(INSTALL_LOG_FILE):
                logFiles = filenames
                break
        return JsonResponse({'logFiles': sorted(logFiles)})

def checkJobStatus(request):
        logger.info(request.body)
        global RUNJOB
        if RUNJOB == None or not RUNJOB.isAlive():
                return JsonResponse({'isalive': False, 'typeofJob': None})
        else:
                return JsonResponse({'isalive': True, 'typeofJob': RUNJOB.returnJobType()})

def activeTables(request):
        logger.info(request.body)
        activeJobs = table.checkTableJobs()
        json = { 'jobs': [] }
        for x in activeJobs:
                json['jobs'].append(x)
        logger.info(json)
        return JsonResponse(json)

def beginInstallPP(request):
        logger.info(request.body)
        global RUNJOB
        global INSTALL_LOG_FILE
        if RUNJOB == None or not RUNJOB.isAlive():
                RUNJOB = beginRunJob('/srv/salt/install.sls', 'Installation', path=INSTALL_LOG_FILE)
                RUNJOB.daemon = True
                RUNJOB.start()
                return JsonResponse({'install': 'Installation started'})
        return JsonResponse({'install': RUNJOB.returnJobType() + ' already running'})

def activeInstallPP(request, position=0):
        global RUNJOB
        if RUNJOB == None or RUNJOB.returnJobType() != "Installation":
                return JsonResponse({})
        json = {'activeInstall': []}
        filename = RUNJOB.getTmpLogFile()
	stageCount = RUNJOB.returnStageCount()
	stagesDone = RUNJOB.returnStageDone()
	json['stageCount'] = stageCount
	json['stagesDone'] = stagesDone
        with open(filename, 'r') as f:
                for i, line in enumerate(f):
                        if i >= int(position):
                                json['activeInstall'].append(line.replace('\n', ''))
        return JsonResponse(json)
