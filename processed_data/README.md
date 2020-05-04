# Processed Data

## Rating file
https://drive.google.com/open?id=1y5f88zJIsDxsnxVRD1dykD9plU2xW2L1


We are running in the mysql workbench environment

method one:

The Run database_query_table.sql file is in mysql. After the file runs, it will automatically generate a Database and all the tables named after the csv file.
Then you can view the columns in the table by writing a query.

use "table name"; 
select "columns name" from "Tables".



For example: 
use 255databse;
select * from cast_info


Due to Method 1 needs to change the path load csv file, so method 2, you can create the databse using 
Method 1 needs to change the path after downloading the csv file, so in method 2, you can create a new schema by clicking the fourth icon in the upper left corner called "create a new schema" database name: 255database.

And then right-click on the Tables in 255database in the left schemas and select table_data_import_wizard. Finally, just click the downloaded csv file in the file path to import successfully
