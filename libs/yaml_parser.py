import sys, os
from libs.db.DBOperations import AppAccessLayer
from libs.db.DBOperations import DWAccessLayer
from libs.db.Config import Config

from libs.common import get_yaml

class yaml_parser:
    def __init__(self, yaml_file):
        yml = get_yaml(yaml_file)
        self.__data_info = yml

        # source
        source_silo_id = yml['source_table']['silo_id']
        source_silo_server = yml['source_table']['silo_server']
        
        source_app_conn = AppAccessLayer(db_name = source_silo_id, rdp_server = source_silo_server)
        source_config = Config(app_connection = source_app_conn, silo_id = source_silo_id)
        self.__data_info['source_table']['server'] = source_config.get_config(["dw.server.name"])["dw.server.name"]
        self.__data_info['source_table']['db'] = source_config.get_config(["dw.db.name"])["dw.db.name"]
        self.__data_info['source_table']['schema'] = source_config.get_config(["dw.schema.name"])["dw.schema.name"]
        self.__data_info['source_table']['username'] = source_config.get_config(["dw.user.id"])["dw.user.id"]
        self.__data_info['source_table']['password'] = source_config.get_config(["dw.user.password"])["dw.user.password"]
        
        # target
        target_silo_id = yml['target_table']['silo_id']
        target_silo_server = yml['target_table']['silo_server']
        
        target_app_conn = AppAccessLayer(db_name = target_silo_id, rdp_server = target_silo_server)
        target_config = Config(app_connection = target_app_conn, silo_id = target_silo_id)
        self.__data_info['target_table']['server'] = target_config.get_config(["dw.server.name"])["dw.server.name"]
        self.__data_info['target_table']['db'] = target_config.get_config(["dw.db.name"])["dw.db.name"]
        self.__data_info['target_table']['schema'] = target_config.get_config(["dw.schema.name"])["dw.schema.name"]
        self.__data_info['target_table']['username'] = target_config.get_config(["dw.user.id"])["dw.user.id"]
        self.__data_info['target_table']['password'] = target_config.get_config(["dw.user.password"])["dw.user.password"]
        
        # close connection
        source_app_conn.close_connection()
        target_app_conn.close_connection()
        
    def get_data_info(self):
        return self.__data_info
        
if __name__ == '__main__':
    y = yaml_parser('D:/Work/tools/data_mover/yamls/ANL_DIM_OSM_CLASSIFICATION.yml')
    print(y.get_data_info()['columns'])