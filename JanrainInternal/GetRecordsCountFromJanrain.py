# Required Imports
import requests
import pandas as pd

__author__ = "sats17"

"""
For more information regarding API refer this url => "https://identitydocs.akamai.com/home/entity-and-entitytype-apis"
Note - Quotes are mandatory for Janrain API attributes,any changes in that can cause API call failure.
"""


class GetRecordsCountFromJanrain:

    def __init__(self, credentialsFilePath):
        """
        Constructor takes CSV file name as parameter and reads the CSV file
        :param credentialsFilePath: CSV File path that use to read and set credentials
        """
        print("Reading credentials From CSV")
        credentialsData = pd.read_csv(credentialsFilePath)
        self.client_id = credentialsData.client_id[0]
        self.client_secret = credentialsData.client_secret[0]
        self.URL = "https://" + credentialsData.url[0]
        self.type_name = credentialsData.type_name[0]

    def getCredentials(self):
        """
        :return: Janrain credentials
        """
        response = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "URL": self.URL,
            "type_name": self.type_name
        }
        return response

    def getCount(self):
        print("Fetching records from Janrain API -> ", self.URL)

        PARAMS = {'client_id': self.client_id, 'client_secret': self.client_secret, 'type_name': self.type_name}
        result = requests.get(url=self.URL + "/entity.count", params=PARAMS)
        data = result.json()
        return data

    def getCountHavingConditionIs(self, queryFilter):
        """
        :param queryFilter: Condition name where count have this condition
        :return: Response of count
        """
        try:
            print("Fetching records from Janrain API -> ", self.URL)
            # Api parameters
            PARAMS = {'client_id': self.client_id, 'client_secret': self.client_secret, 'type_name': self.type_name,
                      'timeout': 120, 'filter': queryFilter}
            response = requests.get(url=self.URL + "/entity.count", params=PARAMS).json()
            return response
        except:
            return "API call fail, please try again."
