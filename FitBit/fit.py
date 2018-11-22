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
auth2_client = fitbit.Fitbit(CLIENT_ID, CLIENT_SECRET, 
        oauth2=True, access_token=ACCESS_TOKEN, 
        refresh_token=REFRESH_TOKEN)

today = datetime.datetime.now()

for i in range(7,12):
    dom = (today - datetime.timedelta(days=i)).strftime("%Y-%m-%d")
    calorie_count = auth2_client.intraday_time_series('activities/tracker/calories', base_date=dom)
    fit_statsHR_heart = auth2_client.intraday_time_series('activities/heart', base_date=dom, detail_level='1min')
    acti = auth2_client.activities(dom)
    print(" ")
    print("Calorie Count: ",calorie_count['activities-tracker-calories'][0]['value'])
    print("HeartRate : FatBurn: ",fit_statsHR_heart['activities-heart'][0]['value']['heartRateZones'][1]['max'])
    print("HeartRate : Cardio: ",fit_statsHR_heart['activities-heart'][0]['value']['heartRateZones'][2]['max'])
    print("HeartRate : Peak: ",fit_statsHR_heart['activities-heart'][0]['value']['heartRateZones'][3]['max'])	
	print("HeartRate : Resting: ", fit_statsHR_heart['activities-heart']['restingHeartRate'])
	print("Distance: ",acti['summary']['distances'][0]['distance'])
    print("Steps: ",acti['summary']['steps'])

