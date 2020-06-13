from JanrainInternal.GetRecordsFromJanrain import GetRecordsFromJanrain
from JanrainInternal.GetRecordsCountFromJanrain import GetRecordsCountFromJanrain
from JanrainInternal.UpdateRecordsInJanrain import UpdateRecordsInJanrain

if __name__ == "__main__":

    ################ Global Settings #####################
    FilePath = 'records.csv'
    CredentialsPath = 'credentials.csv'

    ############### Select Methods ######################33
    GetRecordsObj = GetRecordsFromJanrain(CredentialsPath)
    GetRecordsObj.getCredentials()

