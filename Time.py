import ntplib, datetime
from time import ctime

def get_ntp_time():
    try:
        client = ntplib.NTPClient()
        response = client.request('pool.ntp.org')
        return datetime.datetime.fromtimestamp(response.tx_time)
    except Exception as e:
        print("⚠️ Failed to get NTP time, falling back to device time:", e)
        return datetime.datetime.now()
