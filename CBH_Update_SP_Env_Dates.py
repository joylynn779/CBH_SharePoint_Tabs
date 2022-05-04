from office365.runtime.auth.user_credential import UserCredential
from office365.sharepoint.client_context import ClientContext
import DB_Query

test_server = r'ttmtestapp03\tylerci'
prod_server = r'ttmapp03\tylerci'

muntest_data = DB_Query.get_db_info(test_server, 'muntest', 'Test')
munverif_data = DB_Query.get_db_info(test_server, 'munverif', 'Verif')
muntrain1_data = DB_Query.get_db_info(prod_server, 'muntrain', 'Train 1')
muntrain2_data = DB_Query.get_db_info(prod_server, 'muntrain2', 'Train 2')

server_url = 'https://bevhills-my.sharepoint.com'
site_url = 'https://bevhills.sharepoint.com/sites/zFinance'
username = 'jhayes@beverlyhills.org'
password = 'Brody2love!'
ctx = ClientContext(site_url).with_credentials(UserCredential(username, password))

# 1. Load existing list items
target_list = ctx.web.lists.get_by_title('Munis Test Environments')
list_items = target_list.get_items()
ctx.load(list_items)
ctx.execute_query()

for item in list_items:
    if item.properties['Title'] == 'Test':
        item.set_property('LastRefreshed', muntest_data.refresh_date)
        item.set_property('MunisVersion', muntest_data.munis_version)
        item.update()
        ctx.execute_query()
    if item.properties['Title'] == 'Verif':
        item.set_property('LastRefreshed', munverif_data.refresh_date)
        item.set_property('MunisVersion', munverif_data.munis_version)
        item.update()
        ctx.execute_query()
    if item.properties['Title'] == 'Train':
        item.set_property('LastRefreshed', muntrain1_data.refresh_date)
        item.set_property('MunisVersion', muntrain1_data.munis_version)
        item.update()
        ctx.execute_query()
    if item.properties['Title'] == 'Train 2':
        item.set_property('LastRefreshed', muntrain2_data.refresh_date)
        item.set_property('MunisVersion', muntrain2_data.munis_version)
        item.update()
        ctx.execute_query()

    print(item.properties['ID'], item.properties['Title'], item.properties['LastRefreshed'], item.properties['MunisVersion'])
