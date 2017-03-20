
from libs.db_parser import db_parser

class vertica_parser(db_parser):

    def set_paramters(self):
        #----- used in set_export_command
        # in vertica, | is the default delimiter
        delimiter = self.get_field_delimiter()
        self.__delimiter_opt_exp = ''
        self.__delimiter_opt_imp = ''
        if len(delimiter) != 0:
            self.__delimiter_opt_exp = '-F "%(delimiter)s"' % {'delimiter': delimiter}
            self.__delimiter_opt_imp = '''DELIMITER '%(delimiter)s' ''' % {'delimiter': delimiter}        
        
        #----- used in set_import_command
        if '*' in self.get_target_fields():
            self.__target_table = self.get_target_table_name()
        else:
            #-- quote field name which has blankspace in it.
            target_fields = []
            for field in self.get_target_fields():
                if field.find(' ') != -1:
                    target_fields.append( '\\"' + field + '\\"' )
                else:
                    target_fields.append(field)            
            
            self.__target_table = self.get_target_table_name() + '(' + ','.join(target_fields) + ')'
    
    def set_source_query(self):
        #-- quote field name which has blankspace in it.
        source_fields = []
        for field in self.get_source_fields():
            if field.find(' ') != -1:
                source_fields.append( '\\"' + field + '\\"' )
            else:
                source_fields.append(field)
        
        source_where = self.get_source_where()
        if source_where.find('"') != -1:
            source_where = source_where.replace('"', '\\"')
        
        source_schema = self.get_source_schema()
        source_table = self.get_source_table_name()
        
        self._source_query = 'SELECT ' + ', ' . join(source_fields) + ' FROM ' + source_schema + '.' + source_table + source_where
    
    def set_export_command(self):
        self._export_command = '''vsql -h %(db_server)s -d %(db_name)s -U %(username)s -w %(password)s -o %(out_file)s -c "%(source_query)s" %(delimiter_opt)s -Atq -P footer=off -q ''' % { 
                'db_server': self.get_source_server(), 
                'db_name': self.get_source_db(), 
                'username': self.get_source_username(), 
                'password': self.get_source_password(), 
                'out_file': self.get_out_file(), 
                'source_query': self.get_source_query(),
                'delimiter_opt': self.__delimiter_opt_exp
            }
        
    def set_import_command(self):
        self._import_command = '''vsql -h %(db_server)s -d %(db_name)s -U %(username)s -w %(password)s -c "COPY %(target_table)s FROM LOCAL '%(in_file)s' %(delimiter_opt)s DIRECT" ''' % {
                'db_server': self.get_target_server(), 
                'db_name': self.get_target_db(), 
                'username': self.get_target_username(), 
                'password': self.get_target_password(), 
                'target_table': self.__target_table, 
                'in_file': self.get_out_file(),
                'delimiter_opt': self.__delimiter_opt_imp
            }

        
if __name__ == '__main__':
    from common import get_yaml
    
    data_info = get_yaml('D:/Work/tools/data_mover/yamls/incident.yml')
    
    p = vertica_parser(data_info)
    print(p.get_export_command())
    