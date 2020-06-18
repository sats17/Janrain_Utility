# Required Imports
import requests
import pandas as pd
from JanrainInternal.CommonMethods import CommonMethods
import json

__author__ = "sats17"

"""
For more information regarding API refer this url => "https://identitydocs.akamai.com/home/entity-and-entitytype-apis"
Note - Quotes are mandatory for Janrain API attributes,any changes in that can cause API call failure.
"""


class UpdateRecordsInJanrain():

    def __init__(self, credentialsFileName):
        """
        Constructor takes CSV file name as parameter and reads the CSV file
        :param credentialsFileName:
        """
        print("Reading credentials From CSV")
        credentialsData = pd.read_csv(credentialsFileName)
        self.client_id = credentialsData.client_id[0]
        self.client_secret = credentialsData.client_secret[0]
        self.URL = "https://" + credentialsData.url[0]
        self.type_name = credentialsData.type_name[0]

    def getCredentials(self):
        response = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "URL": self.URL,
            "type_name": self.type_name
        }
        return response

    def updateRecords(self, key_attribute, update_attribute, recordsFileName, searchHeaderName, updateHeaderName):
        """
        This function will update the users, and returns two CSV files. one is users successfully updated and other is if
        users is not found then it will be not update.
        :rtype: None
        :param updateHeaderName:
        :param searchHeaderName:
        :param update_attribute:
        :param recordsFileName:
        :param key_attribute: It is the attribute name of key, e.g - email,uuid.
        :return: CSV Files of users updated and not updated
        """

        print("Fetching records from Janrain API -> ", self.URL)

        # Read data from CSV file
        FileData = pd.read_csv(recordsFileName)

        # Array for storing the Output
        Records_Updated_Arr = []
        Records_Not_Updated_Arr = []

        # Counters
        TotalCount = 0
        RecordUpdatedCount = 0
        RecordFailCount = 0

        # This loop will iterate over the all CSV file data.
        for row in FileData.itertuples():
            searchKey = getattr(row, searchHeaderName)
            key_value = CommonMethods.typeConverter(searchKey)

            # Here we creating python dictonary for field that we want update
            if type(getattr(row, updateHeaderName)) == int:
                updateAttributes = {update_attribute: str(getattr(row, updateHeaderName))}
            else:
                updateAttributes = {update_attribute: getattr(row, updateHeaderName)}

            # Janrain Query params dictonary.
            PARAMS = {'client_id': self.client_id, 'client_secret': self.client_secret, 'key_attribute': key_attribute,
                      'key_value': key_value,
                      'type_name': self.type_name, "attributes": json.dumps(updateAttributes)}

            # Janrain API call.
            try:
                response = requests.get(url=self.URL + "/entity.update", params=PARAMS).json()
            except:
                return "API call fail, please try again"

            print("API RESPONSE --> ", response)
            if response['stat'] == 'ok':
                Records_Updated_Arr.append(row.key)
                RecordUpdatedCount += 1
            else:
                Records_Not_Updated_Arr.append(row.key)
                RecordFailCount += 1
            TotalCount += 1
            print("Total user done = ", TotalCount)

        print("Generating CSV Files...")

        # Writing CSV file with desired output.
        pd.DataFrame(Records_Updated_Arr).to_csv("Janrain_records_updated.csv", index=False)
        pd.DataFrame(Records_Not_Updated_Arr).to_csv("Janrain_records_not_updated.csv", index=False)

        print("Execution Complete")
        Response = {
            'Total_Record_Found_In_Janrain': {
                'Count': RecordUpdatedCount,
                'FileName': "Janrain_records_updated.csv"
            },
            'Total_Record_Not_Found_In_Janrain': {
                'Count': RecordFailCount,
                'FileName': "Janrain_records_not_updated.csv"
            }
        }

        return Response

    def updateRecordsHavingValueIs(self, key_attribute, update_value, recordsFileName, searchHeaderName):
        """
        This function will update the users, and returns two CSV files. one is users successfully updated and other is if
        users is not found then it will be not update.
        :param update_value:
        :rtype: None
        :param searchHeaderName:
        :param recordsFileName:
        :param key_attribute: It is the attribute name of key, e.g - email,uuid.
        :return: CSV Files of users updated and not updated
        """

        print("Fetching records from Janrain API -> ", self.URL)

        # Read data from CSV file
        FileData = pd.read_csv(recordsFileName)

        # Array for storing the Output
        Records_Updated_Arr = []
        Records_Not_Updated_Arr = []

        # Counters
        TotalCount = 0
        RecordUpdatedCount = 0
        RecordFailCount = 0

        # This loop will iterate over the all CSV file data.
        for row in FileData.itertuples():
            searchKey = getattr(row, searchHeaderName)
            key_value = CommonMethods.typeConverter(searchKey)

            # Janrain Query params dictonary.
            PARAMS = {'client_id': self.client_id, 'client_secret': self.client_secret, 'key_attribute': key_attribute,
                      'key_value': key_value,
                      'type_name': self.type_name, "attributes": json.dumps(update_value)}

            # Janrain API call.
            try:
                response = requests.get(url=self.URL + "/entity.update", params=PARAMS).json()
            except:
                return "API call fail, please try again"

            print("API RESPONSE --> ", response)
            if response['stat'] == 'ok':
                Records_Updated_Arr.append(row.key)
                RecordUpdatedCount += 1
            else:
                Records_Not_Updated_Arr.append(row.key)
                RecordFailCount += 1
            TotalCount += 1
            print("Total user done = ", TotalCount)

        print("Generating CSV Files...")

        # Writing CSV file with desired output.
        pd.DataFrame(Records_Updated_Arr).to_csv("Janrain_records_updated.csv", index=False)
        pd.DataFrame(Records_Not_Updated_Arr).to_csv("Janrain_records_not_updated.csv", index=False)

        print("Execution Complete")
        Response = {
            'Total_Record_Found_In_Janrain': {
                'Count': RecordUpdatedCount,
                'FileName': "Janrain_records_updated.csv"
            },
            'Total_Record_Not_Found_In_Janrain': {
                'Count': RecordFailCount,
                'FileName': "Janrain_records_not_updated.csv"
            }
        }

        return Response
