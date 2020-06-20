import requests
import pandas as pd
from JanrainInternal.CommonMethods import CommonMethods
import json

__author__ = "sats17"

"""
For more information regarding API refer this url => "https://identitydocs.akamai.com/home/entity-and-entitytype-apis"
Note - Quotes are mandatory for Janrain API attributes,any changes in that can cause API call failure.
"""


class GetRecordsFromJanrain:

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

    def selectSingleRecordBy(self, key, key_attribute, selectAttributes):
        """
        This function will return all data from Janrain for single user
        :param key_attribute: Field name by key will be search in Janrain
        :param key : It is the value, e.g - user email or user uuid
        :param selectAttributes: Fields that you want to fetch from janrain
        :return : return user data in json format.
        """

        print("Fetching records from Janrain URI => ", self.URL)

        # If key is number then typeConverter will convert to String
        key_value = CommonMethods.typeConverter(key)

        # Dictonary consists Query params for janrain API
        PARAMS = {'client_id': self.client_id, 'client_secret': self.client_secret, 'key_attribute': key_attribute,
                  'key_value': key_value, 'type_name': self.type_name, "attributes": json.dumps(selectAttributes)}

        try:
            # Janrain API call
            response = requests.get(url=self.URL + "/entity", params=PARAMS)
        except:
            return "API Call Failed, please try again."

        # Returns a JSON object of the result
        jsonResponse = response.json()
        if jsonResponse['stat'] == 'ok':
            print(jsonResponse)
            response = {'Message': 'Record found in Janrain', 'Response': jsonResponse['result']}
            return response
        else:
            response = {'Message': 'Record not found in janrain'}
            return response

    def selectMultipleRecordsBy(self, key_attribute, selectAttributes, timeout, searchKeyHeaderName, filePath):
        """
        Bulk select from janrain, fetch all data from janrain and store in CSV file.
        if key not found in janrain then that data will store in another file.
        :param filePath: CSV File path
        :param searchKeyHeaderName: CSV Header name using that records will be read for searching in Janrain
        :param timeout: API Timeout
        :param key_attribute: It is the attribute name of key, e.g - email,uuid
        :param selectAttributes: Fields that you want to fetch from janrain
        :return: Janrain Records Found CSV File and Janrain Records Missing CSV File
        """

        print("Fetching records from Janrain API -> ", self.URL)

        attributes = json.dumps(selectAttributes)

        # Read data from CSV file
        FileData = pd.read_csv(filePath)

        # Array for storing the Output
        Records_Founds_Arr = []
        Records_Missing_Arr = []

        # Counters
        TotalCount = 0
        RecordFoundCount = 0
        RecordNotFoundCount = 0

        # This loop will iterate over the CSV file data.
        for row in FileData.itertuples():

            csvKey = getattr(row, searchKeyHeaderName)

            # typeConverter will convert row.key to string
            key_value = CommonMethods.typeConverter(csvKey)

            # Janrain Api Query Parameters.
            PARAMS = {'client_id': self.client_id, 'client_secret': self.client_secret, 'key_attribute': key_attribute,
                      'key_value': key_value, 'type_name': self.type_name, "attributes": attributes, 'timeout': timeout}

            # Janrain API call
            try:
                response = requests.get(url=self.URL + "/entity", params=PARAMS).json()
            except:
                return "API Fails, please check your credentials"

            # If records found then status will 'ok'.
            if response['stat'] == 'ok':
                """
                If data found in Janrain entity then we are appending Records_Found_Arr with given result.
                """
                consolidated_data = response['result']
                Records_Founds_Arr.append(consolidated_data)
                RecordFoundCount += 1
            else:
                """
                If data not found in Janrain entity then we are appending Records_Not_Found_Arr with given input.
                """
                Records_Missing_Arr.append({'Missing_Records': csvKey})
                RecordNotFoundCount += 1

            TotalCount += 1
            print("Total users scanned - ", TotalCount)
            print("Logging response => ", response, "\n")

        print("Generating CSV Files...\n")

        # Writing CSV file with desired output.
        pd.DataFrame(Records_Founds_Arr).to_csv("Output/Janrain_select_records_found.csv", index=False)
        pd.DataFrame(Records_Missing_Arr).to_csv("Output/Janrain_select_records_missing.csv", index=False)

        Response = {
            'Total_Record_Found_In_Janrain': {
                'Count': RecordFoundCount,
                'FileName': "Janrain_select_records_found.csv"
            },
            'Total_Record_Not_Found_In_Janrain': {
                'Count': RecordNotFoundCount,
                'FileName': "Janrain_select_records_missing.csv"
            }
        }

        return Response

    def fetchAllDataFromEntity(self, first_result, max_result, timeout, totalRecordsInJanrain, selectAttributes):
        """
        Returns all documents from janrain, only 10k documents you can retreive in one hit, we are fetching records by
        sorting uuid, and max timeout for API we declare as 60 seconds.
        :param timeout: Api Call Timeout
        :param first_result: Starting Count of the record from where you will fetch the records.
        :param max_result: Max count that you can fetch records from janrain in one API hit. Default and max - 10K.
        :param totalRecordsInJanrain: Total Records in janrain.
        :param selectAttributes: Fields that you want to fetch from janrain.
        :return: It will append every API hit result in CSV file.
        """
        print("Fetching records from Janrain API -> ", self.URL)

        attributes = json.dumps(selectAttributes)
        TotalFetchedRecords = 0

        # Loop will run till first_result is less than totalRecordsInJanrain
        while first_result < totalRecordsInJanrain:
            # Janrain API Query params, records fetched as sorted uuid.
            PARAMS = {'client_id': self.client_id, 'client_secret': self.client_secret, 'type_name': self.type_name,
                      'timeout': timeout, 'attributes': attributes, "first_result": first_result,
                      "max_results": max_result, 'sort_on': '["uuid"]'}

            # Janrain API call
            try:
                response = requests.get(url=self.URL + "/entity.find", params=PARAMS).json()
            except:
                print("Error => API called failed, due to Timeout issue or any other failure.")
                print("Length of total fetched records counts -> ", first_result)
                print("You can again call method with first_result as this ", first_result, " this value")
                print("Note => Increase ApiTimeout to 120 and decrese the max_result value, so API will run smoothly")
                return

            print("Logging RESPONSE --> ", response)

            fetchedRecordsLen = len(response['results'])

            print("length of total fetched records counts -> ", fetchedRecordsLen)

            # Append result in CSV File
            pd.DataFrame(response['results']).to_csv("Output/AllRecordsFromEntity.csv", mode='a', index=False,
                                                     header=False)
            # Increase the first_result counter to max fetched counts
            first_result += max_result

            # This is counter that till now this much records are fetched, in case of any failure in API you can
            # again call the API with this counter
            print("Total fetched count -->  ", first_result)
            TotalFetchedRecords += fetchedRecordsLen
        print("Fetching Completed")
        Response = {
            'Total_Record_Found_In_Janrain': {
                'Count': TotalFetchedRecords,
                'FileName': "AllRecordsFromEntity.csv"
            }
        }
        return Response

    def fetchAllDataFromEntityWhereConditionIs(self, first_result, max_result, totalRecordsInJanrain, selectAttributes,
                                               queryFilter):
        """
        Returns all documents from janrain, only 10k documents you can retreive in one hit, we are fetching records by
        sorting uuid, and max timeout for API we declare as 60 seconds.
        :param queryFilter: Janrain filters for record fetch conditions.
        :param first_result: Starting Count of the record from where you will fetch the records.
        :param max_result: Max count that you can fetch records from janrain in one API hit. Default and max - 10K
        :param totalRecordsInJanrain: Total Records in janrain.
        :param selectAttributes: Fields that you want to fetch from janrain.
        :return: It will append every API hit result in CSV file.
        """

        print("Fetching records from Janrain API -> ", self.URL)

        attributes = json.dumps(selectAttributes)
        TotalFetchedRecords = 0

        # Loop will run till first_result is less than totalRecordsInJanrain
        while first_result < totalRecordsInJanrain:
            # Janrain API Query params, records fetched as sorted uuid.
            PARAMS = {'client_id': self.client_id, 'client_secret': self.client_secret, 'type_name': self.type_name,
                      'timeout': 120, 'attributes': attributes, "first_result": first_result,
                      "max_results": max_result, 'sort_on': '["uuid"]', 'filter': queryFilter}

            # Janrain API call
            try:
                response = requests.get(url=self.URL + "/entity.find", params=PARAMS).json()
            except:
                print("Error => API called failed, due to Timeout issue or any other failure.")
                print("Length of total fetched records counts -> ", first_result)
                print("You can again call method with first_result as this ", first_result, " this value")
                print("Note => Increase ApiTimeout to 120 and decrese the max_result value, so API will run smoothly")
                return

            print("RESPONSE --> ", response)
            fetchedRecordsLen = len(response['results'])

            print("length of total fetched counts -> ", fetchedRecordsLen)

            # Append result in CSV File
            pd.DataFrame(response['results']).to_csv("Output/JanrainDataHavingConditionIs.csv", mode='a', index=False,
                                                     header=False)
            # Increase the first_result counter to max fetched counts
            first_result += max_result

            TotalFetchedRecords += fetchedRecordsLen

            # This is counter that till now this much records are fetched, in case of any failure in API you can again
            # call
            # the API with this counter
            print("Total fetched count -->  ", first_result)
        print("Fetching Completed")
        Response = {
            'Total_Record_Found_In_Janrain': {
                'Count': TotalFetchedRecords,
                'FileName': "JanrainDataHavingConditionIs.csv"
            }
        }
        return Response


