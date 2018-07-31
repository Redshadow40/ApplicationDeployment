# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
from parser import parseYaml
import threading
import Queue
import subprocess
import salt.runner
import yaml
import tarfile
import time
import os
from tableid import table

def checkVersion():
	if not os.path.isfile('/srv/salt/pp_version'):
		return None
	currentVersion = None
	with open('/srv/salt/pp_version', 'r') as f:
		currentVersion = f.read();
	return currentVersion

def checkInstallFile():
	if not os.path.isfile('/srv/salt/install.sls'):
		return False
	return True

def checkValidationFile():
	if not os.path.isfile('/srv/salt/validation.sls'):
		return False
	return True

def extractPackage(filename):
	packageFile = tarfile.open(name=filename)
        packageFile.extractall(path='/srv/')

class beginRunJob(threading.Thread):
	def __init__(self, installFile, typeofJob, path='', keeplogfile=True, forceContinue=False):
		threading.Thread.__init__(self)
		self.data = parseYaml(open(installFile, 'r'))
		self.typeofJob = typeofJob
		self.deployed = True
		self.keeplogfile = keeplogfile
		self.forceContinue = forceContinue
		self.PATH = path
		self.TMPPATH = '/tmp/'
		self.stagesDone = 0
		if not self.PATH == '' and not os.path.isdir(self.PATH):
      			os.mkdir(self.PATH)
	
	def returnJobType(self):
		return self.typeofJob	

	def returnStageCount(self):
		return len(self.data)

	def returnRunStatus(self):
		return self.deployed

	def deleteLoot(self):
		if os.path.isfile("/srv/salt/loot.sls"):
        		os.remove("/srv/salt/loot.sls")
	
	def returnStageDone(self):
		return self.stagesDone

	def run(self):
		if self.keeplogfile:
			self.logfileName = 'saltinstall.' + time.strftime("%Y-%d-%m.%H-%M-%S", time.localtime())
			self.logfile = open(self.PATH + self.logfileName, 'w')
		self.logfileTmpName = 'saltinstall.' + time.strftime("%Y-%d-%m.%H-%M-%S", time.localtime()) + '.tmp'
		self.logfileTmp = open(self.TMPPATH + self.logfileTmpName, 'w')

		opts = salt.config.master_config('/etc/salt/master')
  		runner = salt.runner.RunnerClient(opts)

		for stage in range(1, len(self.data)+1):
			currentStage= 'stage' + str(stage)
		        name = self.data[currentStage][0]['name']
			try:
                		description = self.data[currentStage][0]['description']
		        except:
                		description = ""
			
			self.writeOutput("-------------------------------------------------------")
			self.writeOutput("Stage " + str(stage)  + ": " + name + " -- started")
			
			if not description == "":
				self.writeOutput("description: " + description)

			if not self.runOrch(runner, self.data[currentStage][1], stage):
				self.deployed = False
				if not self.forceContinue:
                       	 		break
			self.writeOutput(currentStage + ": " + name  + " --  completed")
			self.stagesDone = stage

		if self.deployed:
			if self.typeofJob == "Installation":
				self.writeOutput("Deployment Completed");
			elif self.typeofJob == "Validation":
				self.writeOutput("Validation Completed");
		else:
			if self.typeofJob == "Installation":
                                self.writeOutput("Deployment Failed");
                        elif self.typeofJob == "Validation":
                                self.writeOutput("Validation Failed");
		self.deleteLoot()
		self.logfileTmp.close()
		if self.keeplogfile:
			self.logfile.close()
	
	def writeOutput(self, output, ignoreTmp=False):
		if self.keeplogfile:
			self.logfile.write(output.replace('\\n','\n\t') +'\n')
			self.logfile.flush()
		if not ignoreTmp:
			self.logfileTmp.write(output.replace('\\n','\n\t') +'\n')
	                self.logfileTmp.flush()

	def runOrch(self, runner, tmpData, count):
		with open('/srv/salt/loot.sls', 'w+') as tmpFile:
		        yaml.dump(tmpData, tmpFile, default_flow_style=False)
		ret = None
		trys = 0;
		while ret == None or trys < 3:
			try:
				ret = runner.cmd('state.orchestrate', ['loot'], print_event=False)
			except:
				ret = None
			trys = trys + 1
			if ret == None or not self.isMinionConnected(ret, count):
				while table.checkTableJobs():
					time.sleep(2);		
			else:
				break
		if ret == None:
			self.writeOuput("Salt Master disconnected, cannot complete installation")
			return False
		else:
			return self.checkSaltDeploy(ret, count)

	def isMinionConnected(self, ret, count):
		if ret['retcode'] == 0:
			return True
		
		hostFile = os.popen('cat /etc/hostname')
                hostname = hostFile.read().rstrip()

		if ret['data'][hostname + '_master']['salt_|-state' + str(count) + '_|-state' + str(count) + '_|-state']:
                	tmpret = ret['data'][hostname + '_master']['salt_|-state' + str(count) + '_|-state' + str(count) + '_|-state']
		else:
			return False
		connected = True
		for salt in tmpret:
			if salt == 'changes':
                        	for node in tmpret[salt]['ret']:
                                        if isinstance(tmpret[salt]['ret'][node], bool):
						connected  = False
		return connected

	def getLogFile(self):
		return self.PATH + self.logfileName

	def getTmpLogFile(self):
		return self.TMPPATH + self.logfileTmpName

	def checkSaltDeploy(self, ret, count):
  		tmpret = None
  		hostFile = os.popen('cat /etc/hostname')
  		hostname = hostFile.read().rstrip()

  		Success = False
  		if ret['retcode'] == 0:
        		Success = True;

       		if ret['data'][hostname + '_master']['salt_|-state' + str(count) + '_|-state' + str(count) + '_|-state']:
               		tmpret = ret['data'][hostname + '_master']['salt_|-state' + str(count) + '_|-state' + str(count) + '_|-state']
		if not Success:
			try:
				self.writeOutput("comment - ")
				self.writeOutput(tmpret['comment'])
			except:
				pass
       		for salt in tmpret:
               		if salt == 'changes':
                       		if len(tmpret[salt]) == 0:
                               		self.writeOutput("No changes made")
                       		else:
                               		for node in tmpret[salt]['ret']:
                                       		self.writeOutput("----------------------")
						if isinstance(tmpret[salt]['ret'][node], bool):
							self.writeOutput("failed: " + node + " minion disconnected")
						else:
                                       			self.writeOutput(node + ":")
                                       			for state in tmpret[salt]['ret'][node]:
                                               			tmpstate = tmpret[salt]['ret'][node][state]
                                               			if tmpstate['result']:
                                                       			self.writeOutput(tmpstate['__id__'] + " - passed")
                                               			else:
                                                       			self.writeOutput(tmpstate['__id__'] + " - failed")

								if not len(tmpstate['changes']) == 0:
		                                                        self.writeOutput("changes - ", ignoreTmp=True)
                                                                        self.writeOutput(yaml.safe_dump(tmpstate['changes']), ignoreTmp=True)
								try:
									self.writeOutput("comment - ", ignoreTmp=True)
	                                                               	self.writeOutput("\t" + yaml.safe_dump(tmpstate['comment']), ignoreTmp=True)
								except:
									pass
  		return Success
