import sys, os
from optparse import OptionParser
from subprocess import Popen, PIPE

from libs.vertica_parser import vertica_parser
from libs.yaml_parser import yaml_parser
from libs.common import get_yaml, print_log, warn_log, error_log


actions = {
    'export': [''],
    'import': [''],
    'exportAndImport': ['', '']
}

#-- opts
parser = OptionParser()
parser.add_option("--lib", "-l", dest="lib_name", action="store", type="string")
parser.add_option("--action", "-a", dest="action", action="store", type="string", default='exportAndImport', help='export|import|exportAndImport')
parser.add_option("--source_schema", "-s", dest="source_schema", action="store", type="string")
parser.add_option("--target_schema", "-t", dest="target_schema", action="store", type="string")
(options, args) = parser.parse_args()

curr_path = sys.path[0]
lib_full_name = curr_path + '\\yamls\\' + options.lib_name + '.yml'

#-- paramters checking
if not os.path.exists(lib_full_name):
    raise FileNotFoundError(lib_full_name + ' is not found.')

if not (options.action in actions):
    raise RuntimeError('Action ' + options.action + ' is not valid.')
        
yaml = yaml_parser(lib_full_name)
data_info = yaml.get_data_info()

# source/target schema can be specificed from command line
# this is used in the case that source schema is actaully not the one read from config table
# e.g. we want to source METADATA_WMHUB.CALENDAR, 
# since this table is from hub and there is no custom config table in hub
# we can't get the username/password/schemaname like silo, 
# so we will config silo info in yaml as normal, this silo must be in the same vertica server of METADATA_WMHUB,
# we just use the username/password of silo to get connection info for the hub table
# then use the specified schemaname to get the correct table name
if not (options.source_schema is None or len(options.source_schema) == 0):
    data_info['source_table']['schema'] =  options.source_schema
if not (options.target_schema is None or len(options.target_schema) == 0):
    data_info['target_table']['schema'] =  options.target_schema

    
    
#-- main
ver_psr = vertica_parser(data_info)
    
actions['export'] = [ver_psr.get_export_command()]
actions['import'] = [ver_psr.get_import_command()]
actions['exportAndImport'] = [ver_psr.get_export_command(), ver_psr.get_import_command()]

print_log('Start ' + options.action)
for action_command in actions[options.action]:
    print_log(action_command)
    process = Popen(action_command, shell=True, stdout=PIPE, stderr=PIPE)
    process.wait()
    
    if process.returncode != 0:  
        raise RuntimeError('Command failed, existing...')
    
    print_log('\n' + process.communicate()[0].decode(encoding='utf-8'))

    