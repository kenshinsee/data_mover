Install python via anaconda # otherwise you have to manually install packages sqlalchemy, xml, yaml)
Install pyodbc
Run "python init_env.py" # create data_mover.pth
Create yml file in libs folder, please refer to sample_all_cols.yml(move all the columns), sample_specific_cols.yml(move specific columns)
 - elements in source_table and target_table are very straight forward
 - structure under columns
   columns:
     $target_field_name: # <all_fields> means copy all the fields for the table
       source_field: $source_field_name # <all_fields> means copy all the fields for the table
 - where: used to limit data side when querying source table
 - field_delimiter: specify a delimiter when exporting data
 - out_file: indicate a file for data exporting
Run "python data_mover.py -l $yml_name" # $yml_name doesn't include path and extension, e.g. python data_mover.py -l ANL_FACT_OSM_INCIDENTS
You also can specify schema name rather than using the schema name in core_config table, e.g. python data_mover.py -l ANL_FACT_OSM_INCIDENTS -s WM_SALES_SUPPLYCHAIN_US_PEPSICO

