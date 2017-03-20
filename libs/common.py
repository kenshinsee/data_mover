import sys,os,re,datetime,yaml


def get_yaml(yml_file):
	f = open(yml_file)
	y = yaml.load(f)
	f.close()
	return y
    
#-- define color print class
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
#-- print log  func
def print_log(msg, tee_to_handler=None):
	now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	if not tee_to_handler is None:
		tee_to_handler.write(msg + '\n')
	print(bcolors.OKGREEN + "[" + now + "] " + msg + bcolors.ENDC)

def warn_log(msg, tee_to_handler=None):
	now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	if not tee_to_handler is None:
		tee_to_handler.write(msg + '\n')
	print(bcolors.WARNING + "[" + now + "] " + msg + bcolors.ENDC)

def error_log(msg, tee_to_handler=None):
	now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	if not tee_to_handler is None:
		tee_to_handler.write(msg + '\n')
	print(bcolors.FAIL + "[" + now + "] " + msg + bcolors.ENDC)
