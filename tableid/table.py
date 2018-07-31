from __future__ import unicode_literals

from parser import parseReturn
import salt.client
import salt.runner
import logging
from multiprocessing import Process, Queue

logger = logging.getLogger(__name__)

def tableApplyID(request):
	localSalt = salt.client.LocalClient()
	tables = localSalt.cmd('tc*', 'grains.get', ['entityID'])
	logString = ''
	tableQueue = Queue()
	processes = []
	for table in tables:
		try:
			if not request.POST[table] == '':
				process = Process(target=runTableGrain, args=(tableQueue, localSalt, table, checkEntityID(request.POST[table])))
				process.start()
				processes.append(process)
		except:
			pass
	for process in processes:
		process.join()

	for i in range(tableQueue.qsize()):
		logString += parseReturn(tableQueue.get())
	logger.info(logString)
	return logString

def tableReset(request):
	localSalt = salt.client.LocalClient()
	logString = ''
	tableQueue = Queue()
	processes = []
	for table in request.POST.getlist('tableReset[]'):
		process = Process(target=runTableReset, args=(tableQueue, localSalt, table))
		process.start()
		processes.append(process)
	for process in processes:
		process.join()
	for i in range(tableQueue.qsize()):
                logString += parseReturn(tableQueue.get())
	logger.info(logString)
	return logString

def checkEntityID(entityID):
	if len(entityID) < 2:
		return str('l00' + entityID)
	elif len(entityID) < 3:
		return str('l0' + entityID)
	else:
		return str('l' + entityID)

def checkTableJobs():
	opts = salt.config.master_config('/etc/salt/master')
        runner = salt.runner.RunnerClient(opts)
        ret = runner.cmd('jobs.active', print_event=False)
        activeJobs = set()
        for jobs in ret:
                for runs in ret[jobs]['Running']:
                        for tables in runs:
                                activeJobs.add(tables)
	return activeJobs

def runTableGrain(tableQueue, localSalt, tableName, tableEntity):
	log = localSalt.cmd(tableName, 'grains.set', ['entityID', tableEntity])
	tableQueue.put(log)

def runTableReset(tableQueue, localSalt, tableName):
	log = localSalt.cmd(tableName, 'state.apply', ['tablestate.container'])
	tableQueue.put(log)
