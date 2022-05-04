import pyodbc
from dataclasses import dataclass
import datetime


@dataclass(frozen=True)
class DB_Information:
    db: str
    db_name: str
    refresh_date: str
    munis_version: str
    forms_version: str
    hub_version: str


def get_db_info(server, db_name, db_nickname):
    conn = pyodbc.connect("Driver={SQL Server};"
                          "Server=" + server + ";"
                          "Database=" + db_name + ";"
                          "Trusted_Connection=yes;")

    cursor = conn.cursor()
    table_name = db_name + '.dbo.spsysrec'
    query = '''SELECT ? as 'DB'
    ,RTRIM(client_name) as 'Name'
    ,SUBSTRING(client_name, CHARINDEX('DATABASE', client_name)+9,11) as 'LastRefresh'
    ,SUBSTRING(client_name, CHARINDEX('DATABASE', client_name)+9,3) as 'Month'
    ,SUBSTRING(client_name, CHARINDEX('DATABASE', client_name)+13,2) as 'Day'
    ,SUBSTRING(client_name, CHARINDEX('DATABASE', client_name)+16,4) as 'Year'
    ,CASE WHEN SUBSTRING(client_name, CHARINDEX('DATABASE', client_name)+9,3) = 'Jan' THEN 1
         WHEN SUBSTRING(client_name, CHARINDEX('DATABASE', client_name)+9,3) = 'Feb' THEN 2
         WHEN SUBSTRING(client_name, CHARINDEX('DATABASE', client_name)+9,3) = 'Mar' THEN 3
         WHEN SUBSTRING(client_name, CHARINDEX('DATABASE', client_name)+9,3) = 'Apr' THEN 4
         WHEN SUBSTRING(client_name, CHARINDEX('DATABASE', client_name)+9,3) = 'May' THEN 5
         WHEN SUBSTRING(client_name, CHARINDEX('DATABASE', client_name)+9,3) = 'Jun' THEN 6
         WHEN SUBSTRING(client_name, CHARINDEX('DATABASE', client_name)+9,3) = 'Jul' THEN 7
         WHEN SUBSTRING(client_name, CHARINDEX('DATABASE', client_name)+9,3) = 'Aug' THEN 8
         WHEN SUBSTRING(client_name, CHARINDEX('DATABASE', client_name)+9,3) = 'Sep' THEN 9
         WHEN SUBSTRING(client_name, CHARINDEX('DATABASE', client_name)+9,3) = 'Oct' THEN 10
         WHEN SUBSTRING(client_name, CHARINDEX('DATABASE', client_name)+9,3) = 'Nov' THEN 11
         WHEN SUBSTRING(client_name, CHARINDEX('DATABASE', client_name)+9,3) = 'Dec' THEN 12
        END as 'Month_No'        
    ,RTRIM(sys_rev) as 'Munis_Version'
    FROM dbo.spsysrec
    '''
    cursor.execute(query, [db_nickname])
    result = cursor.fetchall()

    cursor.close()
    conn.close()
    db_details = {}
    for row in result:
        row_refresh_date = datetime.datetime(int(row.Year), int(row.Month_No), int(row.Day), 12, 0, 0)
        pass_date = row_refresh_date.strftime('%Y-%m-%dT%H:%M:%S.%f%z') + 'Z'
        db_details = DB_Information(row.DB, row.Name, pass_date, row.Munis_Version,'','')

    return db_details
