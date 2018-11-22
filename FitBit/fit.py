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

calorie = list()
fatBurnMAX = list()
fatBurnMIN = list()
cardioMAX = list()
cardioMIN = list()
peakMAX=list()
peakMIN=list()
rest = list()
steps =list()
dist = list()
d = list()

for i in range(7,12):
    dom = (today - datetime.timedelta(days=i)).strftime("%Y-%m-%d")
    d.append(dom)
    calorie_count = auth2_client.intraday_time_series('activities/tracker/calories', base_date=dom)
    fit_statsHR_heart = auth2_client.intraday_time_series('activities/heart', base_date=dom, detail_level='1min')
    acti = auth2_client.activities(dom)
    # print(dom)
    # print("Calorie Count: ",calorie_count['activities-tracker-calories'][0]['value'])
    calorie.append(calorie_count['activities-tracker-calories'][0]['value'])
    fatBurnMAX.append(fit_statsHR_heart['activities-heart'][0]['value']['heartRateZones'][1]['max'])
    fatBurnMIN.append(fit_statsHR_heart['activities-heart'][0]['value']['heartRateZones'][1]['min'])
    # print("HeartRate-FatBurn-MAX: ",fit_statsHR_heart['activities-heart'][0]['value']['heartRateZones'][1]['max'], 
	# "MIN: ", fit_statsHR_heart['activities-heart'][0]['value']['heartRateZones'][1]['min'])
    cardioMAX.append(fit_statsHR_heart['activities-heart'][0]['value']['heartRateZones'][2]['max'])
    cardioMIN.append(fit_statsHR_heart['activities-heart'][0]['value']['heartRateZones'][2]['min'])
    # print("HeartRate-Cardio-MAX: ",fit_statsHR_heart['activities-heart'][0]['value']['heartRateZones'][2]['max'],
	# "MIN: ", fit_statsHR_heart['activities-heart'][0]['value']['heartRateZones'][2]['min'])
    peakMAX.append(fit_statsHR_heart['activities-heart'][0]['value']['heartRateZones'][3]['max'])
    peakMIN.append(fit_statsHR_heart['activities-heart'][0]['value']['heartRateZones'][3]['min'])
    # print("HeartRate-Peak-MAX: ",fit_statsHR_heart['activities-heart'][0]['value']['heartRateZones'][3]['max'],
	# "MIN: ", fit_statsHR_heart['activities-heart'][0]['value']['heartRateZones'][3]['min'])	
    rest.append(fit_statsHR_heart['activities-heart'][0]['value']['restingHeartRate'])
    # print("HeartRate-Resting: ", fit_statsHR_heart['activities-heart'][0]['value']['restingHeartRate'])
    dist.append(acti['summary']['distances'][0]['distance'])
    # print("Distance: ",acti['summary']['distances'][0]['distance'])
    steps.append(acti['summary']['steps'])
    # print("Steps: ",acti['summary']['steps'])

