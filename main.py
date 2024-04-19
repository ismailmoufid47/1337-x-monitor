from json import loads
from threading import Timer
from pushbullet import API
from datetime import datetime
from twitter_scraper_selenium import get_profile_details
from requests import request

interval = 10 #seconds

pb = API()
pb.set_token('Your Pushbullet api key')

url = "{{APIUrl}}/waInstance{{idInstance}}/sendMessage/{{apiTokenInstance}}"
headers = {
'Content-Type': 'application/json'
}

def get_post_count():
    profile = loads(get_profile_details("1337FIL"))
    statuses_count = profile["user"]["result"]["legacy"]["statuses_count"]
    return statuses_count


latest_post_count = get_post_count()


def check():
    global latest_post_count
    current_time = datetime.now()

    if current_time.hour >= 10:
        try:
            statuses_count = get_post_count()

            if statuses_count > latest_post_count:
                pb.send_link(
                    "1337 Posted", "Hurry!", "https://candidature.1337.ma/meetings"
                )

                request("POST", url, headers=headers, data=payload)
                request("POST", url, headers=headers, data=payload)
                request("POST", url, headers=headers, data=payload)
                request(
                    "POST",
                    url,
                    headers=headers,
                    data='{\r\n\t"chatId": "120363286086474982@g.us",\r\n\t"message": "this message was sent by a bot"\r\n}',
                )

                latest_post_count = statuses_count
                print(
                    datetime.now(), ": Posted, checking again in ", interval, "seconds"
                )
            elif statuses_count < latest_post_count:
                latest_post_count = statuses_count
                print(
                    datetime.now(),
                    ": deleted post, checking again in ",
                    interval,
                    "seconds",
                )
            else:
                print(
                    datetime.now(),
                    ": Haven't posted, checking again in ",
                    interval,
                    "seconds",
                )
        except Exception as e:
            print("Error: ", e)
            pb.send_note("Caution, Error", str(e))

        Timer(interval, check).start()
    else:
        time_until_10 = (
            current_time.replace(hour=10, minute=0, second=0, microsecond=0)
            - current_time
        ).total_seconds()
        print("Past midnight, checking again until 10am in:", time_until_10, "seconds")
        Timer(time_until_10, check).start()


if __name__ == "__main__":
    check()
