# fedex_tracking_day
Slim python API to wrap using the FedEx Tracking Number API. NOTE:: **you must create your own fedex API developers account to request valid credentials in order to use this package**.

# Quick Start

## Prerequisites
### OS
* MAC or Linux

### FedEx Api Credentials
* Follow the instructions [HERE](https://developer.fedex.com/api/en-us/get-started.html) to get appropriate credentials.
  * Follow all steps:
    * create a fedex developer account.
    * create an organization for your new account.
    * create a project w/in the new organization just created.
    * (optional?) add a user to this project just created.
    * Request [Track API](https://developer.fedex.com/api/en-us/catalog/track.html) credentials.
      * You will initially be provisioned SANDBOX credentials, which will not work with fedex tracking numbers issued in real life.
    * Request your Track API credentials be provisioned for use in `production`.


### Save API Credentials To A ~/.config/fedex/fedex_prod.yaml File
* See [yaml_config_day](https://github.com/Daylily-Informatics/yaml_config_day) for more detail on `yaml_config_day` and how it manages yaml config files.
  * Once you have your production API credentials issued, save them in a file located: `~/.config/fedex/fedex_prod.yaml`. With the contents:
  ```text
  ---
  api_url: https://apis.fedex.com/oauth/token
  client_id: ..................................
  client_secret: ................................
  ```

## Install With Pip
Requires python >= 3.10 & pip.

```bash
pip install fedex_track_day
```

## Track A FedEx Tracking Number (valid)

From the cloned repository directory. Given a VALIDbc, one which has been `Delivered`.
```bash
python fedex_tracking_day/fedex_track.py VALIDbc

# <__main__.FedexTrack object at 0x1030f70e0>
# {'Pickup_dt': '2023-06-26T17:12:00+00:00', 'Delivery_dt': '2023-06-27T11:34:00+00:00', 'Tender_dt': '', 'Ship_dt': '2023-06-26T00:00:00-06:00', 'Transit_Time_sec': '', 'Delivery_Status': 'Delivered', 'Origin_state': 'CA', 'Destination_state': 'CA', 'Delivery_weekday': 'Tuesday', 'Ship_weekday': ''}

# Delivery Status For VALIDbc ... is ... Delivered

```

## Track A FedEx Tracking Number (invalid or expired)
Tracking numbers can not be queried for ever, at some point (>1r?) FedEx will no longer return tracking info for a previously used number.
**WARNING** FedEx will, in fact, re-use tracking numbers, after some amount of time.  I do not believe it is safe to assume fedex tracking numbers may be used as GUIDs.

From the cloned repository directory. Given an invalid, or expired, tracking number, an empty dictionary is returned, and the delivery status is `na`.
```bash
python fedex_tracking_day/fedex_track.py INVALIDbc

# <__main__.FedexTrack object at 0x1056470e0>
# {'Pickup_dt': '', 'Delivery_dt': '', 'Tender_dt': '', 'Ship_dt': '', 'Transit_Time_sec': -1, 'Delivery_Status': 'na', 'Origin_state': 'na', 'Destination_state': 'na', 'Delivery_weekday': '', 'Ship_weekday': ''}

# Delivery Status For INVALIDbc ... is ... na
```

# Development Use

## Create `~/.config/fedex/fedex_prod.yaml` FedEx API Credentials File
As described above.

## Clone Head
`git clone git@github.com:Daylily-Informatics/fedex_tracking_day.git`

## Move Into Repository
`cd fedex_tracking_day`

## Create Development Env
Using [mamnba](https://anaconda.org/conda-forge/mamba).

`mamba env create -n DFEDEX -f DFEDEX.yaml`

## Run Simple Single Tracking Number Query (Invalid Track Number)

`python fedex_tracking_day/fedex_track.py INVALIDbc`


## Via IPython Shell

`ipython`

### Query A Tracking Number Programatically
#### INVALID BARCODE - FULL API DATA
```python
import fedex_tracking_day.fedex_track as FTD
track_d = FTD.FedexTrack()
track_d.get_fedex_json('invalid')
# Out[4]:
# {'transactionId': '482f7886-f118-441b-b7b9-4db4bc462ff1',
#  'output': {'completeTrackResults': [{'trackingNumber': 'invalid',
#    'trackResults': [{'trackingNumberInfo': {'trackingNumber': 'invalid',
#       'trackingNumberUniqueId': '',
#       'carrierCode': ''},
#      'error': {'code': 'TRACKING.TRACKINGNUMBER.NOTFOUND',
#       'message': 'Tracking number cannot be found. Please correct the tracking number and try again.'}}]}]}}
```


#### VALID BARCODE - FULL API	DATA
```python
track_d.get_fedex_json('VALIDfedexTRACKnumber')
```

Which will return  (specifics for the valid tracking number are **REDACTEDREDACTED**).

```python
{
    "transactionId": "REDACTEDREDACTED",
    "output": {
        "completeTrackResults": [
            {
                "trackingNumber": "REDACTEDREDACTED",
                "trackResults": [
                    {
                        "trackingNumberInfo": {
                            "trackingNumber": "REDACTEDREDACTED",
                            "trackingNumberUniqueId": "REDACTEDREDACTED",
                            "carrierCode": "FDXE"
                        },
                        "additionalTrackingInfo": {
                            "nickname": "",
                            "packageIdentifiers": [
                                {
                                    "type": "SHIPPER_REFERENCE",
                                    "values": [
                                        "REDACTEDREDACTED"
                                    ],
                                    "trackingNumberUniqueId": "",
                                    "carrierCode": ""
                                }
                            ],
                            "hasAssociatedShipments": false
                        },
                        "shipperInformation": {
                            "address": {
                                "city": "VALENCIA",
                                "stateOrProvinceCode": "CA",
                                "countryCode": "US",
                                "residential": false,
                                "countryName": "United States"
                            }
                        },
                        "recipientInformation": {
                            "address": {
                                "city": "OAKLAND",
                                "stateOrProvinceCode": "CA",
                                "countryCode": "US",
                                "residential": false,
                                "countryName": "United States"
                            }
                        },
                        "latestStatusDetail": {
                            "code": "DL",
                            "derivedCode": "DL",
                            "statusByLocale": "Delivered",
                            "description": "Delivered",
                            "scanLocation": {
                                "residential": false
                            }
                        },
                        "dateAndTimes": [
                            {
                                "type": "ACTUAL_PICKUP",
                                "dateTime": "2023-06-26T17:12:00+00:00"
                            },
                            {
                                "type": "ACTUAL_DELIVERY",
                                "dateTime": "2023-06-27T11:34:00+00:00"
                            },
                            {
                                "type": "SHIP",
                                "dateTime": "2023-06-26T00:00:00-06:00"
                            }
                        ],
                        "availableImages": [],
                        "specialHandlings": [
                            {
                                "type": "DELIVER_WEEKDAY",
                                "description": "Deliver Weekday",
                                "paymentType": "OTHER"
                            },
                            {
                                "type": "RESIDENTIAL_DELIVERY",
                                "description": "Residential Delivery",
                                "paymentType": "OTHER"
                            }
                        ],
                        "packageDetails": {
                            "packagingDescription": {
                                "type": ""
                            }
                        },
                        "shipmentDetails": {
                            "possessionStatus": true
                        },
                        "scanEvents": [
                            {
                                "date": "2023-06-27T11:34:00+00:00",
                                "eventType": "DL",
                                "eventDescription": "Delivered",
                                "exceptionCode": "02",
                                "exceptionDescription": " Package delivered to recipient address - release authorized",
                                "scanLocation": {
                                    "streetLines": [
                                        ""
                                    ],
                                    "city": "OAKLAND",
                                    "stateOrProvinceCode": "CA",
                                    "postalCode": "REDACTEDREDACTED",
                                    "countryCode": "US",
                                    "residential": false
                                },
                                "locationId": "JBSA",
                                "locationType": "DELIVERY_LOCATION",
                                "derivedStatusCode": "DL",
                                "derivedStatus": "Delivered"
                            }
                        ],
                        "availableNotifications": [],
                        "deliveryDetails": {
                            "actualDeliveryAddress": {
                                "city": "OAKLAND",
                                "stateOrProvinceCode": "CA",
                                "countryCode": "US",
                                "residential": false,
                                "countryName": "United States"
                            },
                            "deliveryAttempts": "0",
                            "deliveryOptionEligibilityDetails": [
                                {
                                    "option": "INDIRECT_SIGNATURE_RELEASE",
                                    "eligibility": "INELIGIBLE"
                                },
                                {
                                    "option": "REDIRECT_TO_HOLD_AT_LOCATION",
                                    "eligibility": "INELIGIBLE"
                                },
                                {
                                    "option": "REROUTE",
                                    "eligibility": "INELIGIBLE"
                                },
                                {
                                    "option": "RESCHEDULE",
                                    "eligibility": "INELIGIBLE"
                                },
                                {
                                    "option": "RETURN_TO_SHIPPER",
                                    "eligibility": "INELIGIBLE"
                                },
                                {
                                    "option": "DISPUTE_DELIVERY",
                                    "eligibility": "INELIGIBLE"
                                },
                                {
                                    "option": "SUPPLEMENT_ADDRESS",
                                    "eligibility": "INELIGIBLE"
                                }
                            ]
                        },
                        "originLocation": {
                            "locationContactAndAddress": {
                                "address": {
                                    "city": "VALENCIA",
                                    "stateOrProvinceCode": "CA",
                                    "countryCode": "US",
                                    "residential": false,
                                    "countryName": "United States"
                                }
                            },
                            "locationId": "VNYA"
                        },
                        "destinationLocation": {
                            "locationContactAndAddress": {
                                "address": {
                                    "city": "OAKLAND",
                                    "stateOrProvinceCode": "CA",
                                    "countryCode": "US",
                                    "residential": false,
                                    "countryName": "United States"
                                }
                            },
                            "locationType": ""
                        },
                        "serviceDetail": {
                            "type": "FEDEX_2_DAY",
                            "description": "FedEx 2Day",
                            "shortDescription": "P-2"
                        },
                        "standardTransitTimeWindow": {
                            "window": {}
                        },
                        "estimatedDeliveryTimeWindow": {
                            "window": {}
                        },
                        "goodsClassificationCode": "",
                        "returnDetail": {}
                    }
                ]
            }
        ]
    }
}
```

#### VALID BARCODE - SUMMARIZED DATA METHOD BEHAVIOR
```python
json.dumps(track_d.get_fedex_ops_meta_ds('780351469400'), indent=4)
```

Returns
```python
{
"Pickup_dt": "2023-06-26T17:12:00+00:00",
"Delivery_dt": "2023-06-27T11:34:00+00:00",
"Tender_dt": "",
"Ship_dt": "2023-06-26T00:00:00-06:00",
"Transit_Time_sec": "",
"Delivery_Status": "Delivered",
"Origin_state": "CA",
"Destination_state": "CA",
"Delivery_weekday": "Tuesday",
"Ship_weekday": ""
}
```

