from __future__ import unicode_literals

from parser import parseYaml
import logging
logger = logging.getLogger(__name__)
import yaml
import os

def getSiteSurvey():
	try:
		siteFile = open('/srv/pillar/sitesurvey.sls', 'r')
		siteData = parseYaml(siteFile)
        	siteFile.close()
		logger.info(siteData)
		return siteData
	except:
		logger.error('/srv/pillar/sitesurvey.sls file not found')
	return None

def createSiteTable(data, unique=''):
	tableText = ''
	for key in data:
		if isinstance(data[key], dict):
			tableText += '<tr><td><strong>' + key + ':</strong></td></tr>'
                        tableText += '<tr><td><table class="table table-striped">' + createSiteTable(data[key], unique=unique+key) + '</table></td></tr>'
		else:
			try:
				if 'password' in key:
					tableText += '<tr><td>' + key + '</td><td><input class="surveyInput" style="float: right;" type="password" name="' + unique + key + '" value="' + str(data[key]) + '"></input></td></tr>'
				else:
					tableText += '<tr><td>' + key + '</td><td><input class="surveyInput" style="float: right;" type="text" name="' + unique + key + '" value="' + str(data[key]) + '"></input></td></tr>'
			except:
				pass
	return tableText

def saveSiteSurvey(request):
	siteData = getSiteSurvey()
	newSiteData = changeSiteValue(siteData, request)
	with open('/srv/pillar/sitesurvey.sls', 'w+') as tmpFile:
		yaml.safe_dump(newSiteData, tmpFile, default_flow_style=False)
		

def changeSiteValue(data, request, unique=''):
	for key in data:
		if isinstance(data[key], dict):
			data[key] = changeSiteValue(data[key], request, unique=unique+key)
		else:
			try:
				data[key] = request.POST[unique+key]
			except:
				pass
	return data	
