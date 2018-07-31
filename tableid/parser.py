from __future__ import unicode_literals

from salt.utils.yamlloader import SaltYamlSafeLoader
import yaml

def parseReturn(ret):
	retString = ""
        for table in ret:
		retString += table + ":<br>"
		if 'result' in ret[table]:
			retString += parseTable(ret[table])
		else:
			for item in ret[table]:
				if 'result' in ret[table][item]:
					retString += parseTable(ret[table][item], orch=True)
	return retString

def parseTable(ret, orch=False):
	tab = '<div style="padding-left: 15px;">'
	closetab = '</div>'
	retString = ""
	if orch:
		if ret['result']:
			retString += tab + '<font color="green">' + ret['name']
			retString += ' - passed</font><br>'
		else:
			retString += tab + '<font color="red">' + ret['name']
			retString += ' - failed</font><br>'
		retString += closetab
	else:
        	if ret['result']:
			retString += tab + '<font color="green">' + 'command'
                	retString += ' - passed</font><br>'
        	else:
			retString += tab + '<font color="red">' + 'command'
                	retString += ' - failed</font><br>'
		for command in ret['changes']:
			retString += tab + command + " -- " + ret['changes'][command] + closetab
		retString += closetab	
	return retString 	

def parseYaml(yaml_data):
  	if not isinstance(yaml_data, basestring):
        	yaml_data = yaml_data.read()
  	data = yaml.load(yaml_data, Loader=SaltYamlSafeLoader)
  	return data if data else {}
