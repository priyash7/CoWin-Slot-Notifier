import requests
from datetime import datetime
import schedule
import time

cowin_api = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict"
now = datetime.now()
current_date = now.strftime("%d-%m-%Y")
telegram_api = "https://api.telegram.org/bot1837680589:AAEL8W6k_qo7RvYzRsueJRJWMtuDBao9YTw/sendMessage?chat_id=@__groupid__&text="
telegram_id = "co_win_slots_notifier"
state_district_ids = [240,241,242,243,244,245,246,247,248,249,250,251,252,253,254,255,256,257,258,259,260,261,262,263,82,100,97,265,276,294,287,292,725] 

#for sending message in telegram
def telegram_notification(message):
	telegram_url = telegram_api.replace("__groupid__", telegram_id)
	telegram_url = telegram_url + message
	response = requests.get(telegram_url)
	print(response)

#for extracting availabilty of data
def available_data(response):
	response_json = response.json()
	for center in response_json["centers"]:
		for session in center["sessions"]:
			if session["available_capacity_dose1"] > 0 and session["min_age_limit"]==18:
				message = "Pincode: {}, Center Name: {}, Slots: {}, Minimum Age: {}".format(center["pincode"], center["name"], session["available_capacity_dose1"], session["min_age_limit"])
				telegram_notification(message)

#for extracting data from CoWin
def cowin_data(district_id):
	query_params = "?district_id={}&date={}".format(district_id, current_date)
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
	main_url = cowin_api+query_params
	response = requests.get(main_url, headers=headers)
	available_data(response)
	# print(response.text)

#fetching data for state
def state_data(district_ids):
	for district_id in district_ids:
		cowin_data(district_id)

#for manually running task
#if __name__ == "__main__":
	#state_data(state_district_ids)

#for automating task
if __name__ == "__main__":
	schedule.every(30).minutes.do(state_data , district_id=state_district_ids)
	while 1:
		schedule.run_pending()
		time.sleep(1)