import fitbit
import gather_keys_oauth2 as Oauth2
import datetime
import json

CLIENT_ID  = '22D6DJ'
CLIENT_SECRET = '0742b59151956ab1351144352675aaf5'

server = Oauth2.OAuth2Server(CLIENT_ID, CLIENT_SECRET)
server.browser_authorize()

ACCESS_TOKEN = str(server.fitbit.client.session.token['access_token'])
REFRESH_TOKEN = str(server.fitbit.client.session.token['refresh_token'])
a2c = fitbit.Fitbit(CLIENT_ID, CLIENT_SECRET, 
        oauth2=True, access_token=ACCESS_TOKEN, 
        refresh_token=REFRESH_TOKEN)

today = datetime.datetime.now()
dom = (today - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
fit_statsHR = a2c.intraday_time_series('activities/heart', base_date=dom, detail_level='1sec')

print(act = a2c.activities())

# for i in range(1,8):
# 	dom = (today - datetime.timedelta(days=i)).strftime("%Y-%m-%d")
# 	print(dom)
# 	fit_statsHR = auth2_client.intraday_time_series('activities/heart', base_date=dom, detail_level='1sec')
# 	print(auth2_client.activities())

