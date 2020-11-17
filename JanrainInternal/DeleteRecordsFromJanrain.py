import pandas as pd
import requests
from JanrainInternal.CommonMethods import CommonMethods


class DeleteRecordsFromJanrain:

    def __init__(self, credentialsFilePath):
        """
        Constructor takes CSV file name as parameter and reads the CSV file
        :param credentialsFilePath: CSV File path that use to read and set credentials
        """
        print("Reading credentials From CSV")
        credentialsData = pd.read_csv(credentialsFilePath)
        self.client_id = credentialsData.client_id[0].strip()
        self.client_secret = credentialsData.client_secret[0].strip()
        self.URL = "https://" + credentialsData.url[0].strip()
        self.type_name = credentialsData.type_name[0].strip()

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

    def bulkDelete(self, key_attribute, deleteKeyHeaderName, recordsFileName):
        """
        This function deletes the users from janrain.
        :param deleteKeyHeaderName: key name use for reading csv header value
        :param recordsFileName: file name
        :param key_attribute: It is the attribute name of key, e.g - email,dcsId.
        :return: CSV Files of users deleted and not deleted
        """

        print("Deleting records from Janrain API -> ", self.URL)

        # Read data from CSV file
        FileData = pd.read_csv(recordsFileName)

        # Array for storing the Output
        Records_Deleted_Arr = []
        Records_Not_Deleted_Arr = []

        # Counters
        totalCount = 0
        recordDeletedCount = 0
        recordFailCount = 0

        # This loop will iterate over the all CSV file data.
        for row in FileData.itertuples():

            deleteKey = getattr(row, deleteKeyHeaderName)

            # typeConverter will convert row.key to string
            key_value = CommonMethods.typeConverter(deleteKey)

            # Query params
            PARAMS = {'client_id': self.client_id, 'client_secret': self.client_secret, 'key_attribute': key_attribute,
                      'key_value': key_value, 'type_name': self.type_name}

            # Janrain API call
            try:
                response = requests.get(url=self.URL + "/entity.delete", params=PARAMS).json()
            except:
                return "API Call  Fails, please check your credentials"

            if response['stat'] == 'ok':
                Records_Deleted_Arr.append(deleteKey)
                recordDeletedCount += 1
            else:
                Records_Not_Deleted_Arr.append(deleteKey)
                recordFailCount += 1
            totalCount += 1
            print("Total users checked/deleted = ", totalCount)
            print("Logging response => ", response, "\n")

        print("Generating CSV Files...")

        # Writing CSV file with desired output.
        pd.DataFrame(Records_Deleted_Arr).to_csv("Output/Janrain_records_deleted.csv", index=False)
        pd.DataFrame(Records_Not_Deleted_Arr).to_csv("Output/Janrain_records_not_deleted.csv", index=False)

        Response = {
            'Total_Record_Deleted_In_Janrain': {
                'Count': recordDeletedCount,
                'FileName': "Janrain_records_deleted.csv"
            },
            'Total_Record_Not_Deleted_In_Janrain': {
                'Count': recordFailCount,
                'FileName': "Janrain_records_not_deleted.csv"
            }
        }

        return Response

