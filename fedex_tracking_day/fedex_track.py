import os
import sys
import time
import requests
import json

import yaml_config_day.config_manager as YCM

from datetime import datetime, timedelta
import pytz


class FedexTrack:

    def __init__(self, config_proj_name='fedex', config_proj_env='prod'):
        yconfig = YCM.ProjectConfigManager(config_proj_name, config_proj_env)
        yconfig_ds = yconfig.get_config()
        
        self.url = yconfig_ds['api_url']
        self.cdict =  {'client_id' : yconfig_ds['client_id'], 'client_secret' : yconfig_ds['client_secret'] }
        self.payload={"grant_type": "client_credentials",'client_id':self.cdict['client_id'],'client_secret':self.cdict['client_secret']}

        self.headers = {'Content-Type': "application/x-www-form-urlencoded"}
        self.response= requests.post(self.url, data=(self.payload), headers=self.headers)

    def auth_token(self):
        token = json.loads(self.response.text)['access_token']
        return token

    
    def get_ship_info(self,ti=None):
        payload = {
            "includeDetailedScans": 'true',
            "trackingInfo": [
                {
                    "trackingNumberInfo": {
                        "trackingNumber": f"{ti}"
                    }
                }
            ]
        }

        url = "https://apis.fedex.com/track/v1/trackingnumbers"
        token = self.auth_token()
        headers = {
            'Content-Type': "application/json",
            'X-locale': "en_US",
            'Authorization': 'Bearer '+ token
        }
        self.ti_response = requests.post(url, data=json.dumps(payload), headers=headers)

        return self.ti_response

    # Returns ALL of the fedex dict of info for this tracking number, if any.  Direct from the fedex api.
    def get_fedex_json(self, ti):
        return self.get_ship_info(ti).json()


    # Returns a pre-processed smaller dictionary of fedex info for this tracking number, with missing data handled consistently.
    def get_fedex_ops_meta_ds(self, ti):
        fedex_json_tmp = self.get_fedex_json(ti)

        weekday_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

        oritin_state = ''
        try:
            origin_state = fedex_json_tmp['output']['completeTrackResults'][0]['trackResults'][0]['originLocation']['locationContactAndAddress']['address']['stateOrProvinceCode']
        except Exception as e:
            return {
                'Pickup_dt' : '',
                'Delivery_dt' : '',
                'Tender_dt' : '',
                'Ship_dt' : '',
                'Transit_Time_sec' : -1,
                'Delivery_Status' : 'na',
                'Origin_state' : 'na',
                'Destination_state' : 'na',
                'Delivery_weekday' : '',
                'Ship_weekday' : '',
            }

        dest_state = ''
        try:
            dest_state = fedex_json_tmp['output']['completeTrackResults'][0]['trackResults'][0]['destinationLocation']['locationContactAndAddress']['address']['stateOrProvinceCode']
        except Exception as e:
            pass

        delivery_status = ''
        try:
            delivery_status = fedex_json_tmp['output']['completeTrackResults'][0]['trackResults'][0]['latestStatusDetail']['statusByLocale']
        except Exception as e:
            pass
        act_pu_dt = ""
        act_delivery_dt = ""
        ship_dt = ""
        act_tender_dt = ""
        transit_time_sec = ""
        delivery_weekday = ''
        ship_weekday = ""
        tender_datetime = ''
        tender_weekday = ''
        try:
            for st in fedex_json_tmp['output']['completeTrackResults'][0]['trackResults'][0]['dateAndTimes']:
                if 'ACTUAL_DELIVERY' in st['type']:
                    act_delivery_dt = st['dateTime']
                    delivery_datetime = datetime.fromisoformat(act_delivery_dt)
                    delivery_weekday = weekday_names[delivery_datetime.weekday()]
                elif 'ACTUAL_PICKUP' in st['type']:
                    act_pu_dt = st['dateTime']
                elif 'SHIP' in st['type']:
                    ship_dt = st['dateTime']
                    ship_datetime = datetime.fromisoformat(ship_dt)
                    ship_weekday = weekday_names[ship_datetime.weekday()]
                elif 'ACTUAL_TENDER' in st['type']:
                    act_tender_dt = st['dateTime']
                    tender_datetime = datetime.fromisoformat(ship_dt)
                    tender_weekday = weekday_names[ship_datetime.weekday()]
        except Exception as e:
            pass

        if ship_dt not in [''] and act_delivery_dt not in [''] and act_tender_dt not in ['']:
            time_delta = datetime.fromisoformat(act_delivery_dt)-datetime.fromisoformat(act_tender_dt)
            transit_time_sec = time_delta.total_seconds()
            
        fedex_json = {
            'Pickup_dt' : act_pu_dt,
            'Delivery_dt' : act_delivery_dt,
            'Tender_dt' : act_tender_dt,
            'Ship_dt' : ship_dt,
            'Transit_Time_sec' : transit_time_sec,
            'Delivery_Status' : delivery_status,
            'Origin_state' : origin_state,
            'Destination_state' : dest_state,
            'Delivery_weekday' : delivery_weekday,
            'Ship_weekday' : tender_weekday,
        }

        return fedex_json



def main(track_number=""):
    fedex_track = FedexTrack('fedex','prod')

    print(fedex_track)

    # fedex_raw_json = fedex_track.get_fedex_json(track_number)

    fetmd = fedex_track.get_fedex_ops_meta_ds(track_number)

    print(fetmd)
    
    print(f"\n\nDelivery Status For {track_number} ... is ... {fetmd['Delivery_Status']} \n")


# When run, will return the processed fedex dict for a given tracking number, as well as the delivery status.
if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise Exception("The first argument to this tool must be a fedex tracking number.")
    
    fedex_track_number = sys.argv[1]
    main(fedex_track_number)