from json import loads
from threading import Timer, Thread
from pushbullet import API
from datetime import datetime
from twitter_scraper_selenium import get_profile_details

pb = API()
pb.set_token('your pushbullet api key')
post_count = 6118
interval = 10 #seconds

def check():
    global post_count
    global interval
    current_time = datetime.now()
    if current_time.hour >= 5:
        try:
            profile = loads(get_profile_details('1337FIL'))
            statuses_count = profile['user']['result']['legacy']['statuses_count']
            
            if statuses_count > post_count:
                post_count += 1
                print(datetime.now(), ': Posted, checking again in ', interval, 'seconds')
                if datetime.now() > last_week:
                    # Send a link notification
                    pb.send_link("1337 Posted", "Hurry!", "https://candidature.1337.ma/meetings")
            elif statuses_count < post_count:
                print(datetime.now(), ': deleted post, checking again in ', interval, 'seconds')
                post_count = statuses_count
            else:
                print(datetime.now(), ": Haven't posted, checking again in ", interval, "seconds")
        except Exception as e:
            print("Error: ", e)
            pb.send_note("Caution, Error", str(e))
            
        # Start the timer again with the updated interval
        Timer(interval, check).start()
    else:
        time_until_5 = current_time.replace(hour=5, minute=0, second=0, microsecond=0) - current_time
        time.sleep(time_until_5.total_seconds())
        check()

if __name__ == "__main__":
    check()
