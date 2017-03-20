
from abc import ABCMeta, abstractmethod

class db_parser:
    __metaclass__ = ABCMeta

    def __init__(self, data_info):
        # source vars
        self.__source_table_name = data_info['source_table']['name']
        self.__source_type = data_info['source_table']['type']
        self.__source_schema = data_info['source_table']['schema']
        self.__source_server = data_info['source_table']['server']
        self.__source_db = data_info['source_table']['db']
        self.__source_username = data_info['source_table']['username']
        self.__source_password = data_info['source_table']['password']
        # target vars
        self.__target_table_name = data_info['target_table']['name']
        self.__target_type = data_info['target_table']['type']
        self.__target_schema = data_info['target_table']['schema']
        self.__target_server = data_info['target_table']['server']
        self.__target_db = data_info['target_table']['db']
        self.__target_username = data_info['target_table']['username']
        self.__target_password = data_info['target_table']['password']
        
        self.__column_map = data_info['columns']
        self.__out_file = data_info['out_file']

        # optional vars
        self.__where = ' WHERE ' + data_info['where'] if 'where' in data_info else ''
        self.__field_delimiter = data_info['field_delimiter'] if 'field_delimiter' in data_info else ''
        
        # set in abstractmethod
        self._export_command = ''
        self._import_command = ''
        
        self.set_field_lists()
        self.set_source_query()
        self.set_paramters()
        self.set_export_command() #abstractmethod
        self.set_import_command() #abstractmethod
        
    def set_field_lists(self):
        self.__target_fields = []
        self.__source_fields = []
        
        for target_field in self.__column_map:
            source_field = ''
            if 'convertion' in self.__column_map[target_field]:
                source_field = self.__column_map[target_field]['convertion'] + ' AS ' + self.__column_map[target_field]['source_field']
            else:
                source_field = self.__column_map[target_field]['source_field']
                        
            if source_field == '<all_fields>':
                self.__target_fields = ['*']
                self.__source_fields = ['*']
                break
            else:
                self.__target_fields.append(target_field) 
                self.__source_fields.append(source_field)
    
    def set_source_query(self):
        self._source_query = 'SELECT ' + ', ' . join(self.__source_fields) + ' FROM ' + self.__source_schema + '.' + self.__source_table_name + self.__where
    
    def set_paramters(self):
        # not force implement, it's could be used to prepare something before executing set_export_command or set_import_command
        pass
        
    @abstractmethod
    def set_export_command(self): 
        # this method must be implemented in child class
        # in the child class _export_command must be correctly set
        # this var is a executable shell/cmd command will be used to export data.
        pass
        
    @abstractmethod
    def set_import_command(self): 
        # this method must be implemented in child class
        # in the child class _import_command must be correctly set
        # this var is a executable shell/cmd command will be used to import data.
        pass
       
    def get_source_fields(self): 
        return self.__source_fields
        
    def get_source_schema(self):
        return self.__source_schema
        
    def get_source_table_name(self):
        return self.__source_table_name
        
    def get_source_where(self):
        return self.__where
       
    def get_source_query(self):
        return self._source_query
        
    def get_source_type(self):
        return self.__source_type
        
    def get_source_server(self):
        return self.__source_server
        
    def get_source_db(self):
        return self.__source_db
    
    def get_source_username(self):
        return self.__source_username
    
    def get_source_password(self):
        return self.__source_password
    
    def get_target_fields(self): 
        return self.__target_fields
        
    def get_target_table_name(self):
        return self.__target_schema + '.' + self.__target_table_name
        
    def get_target_type(self):
        return self.__target_type
        
    def get_target_server(self):
        return self.__target_server
    
    def get_target_db(self):
        return self.__target_db
    
    def get_target_username(self):
        return self.__target_username
    
    def get_target_password(self):
        return self.__target_password
    
    def get_export_command(self):
        return self._export_command
            
    def get_import_command(self):
        return self._import_command
    
    def get_field_delimiter(self):
        return self.__field_delimiter
        
    def get_out_file(self):
        return self.__out_file
    
    