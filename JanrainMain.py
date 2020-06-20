from JanrainInternal.GetRecordsFromJanrain import GetRecordsFromJanrain
from JanrainInternal.GetRecordsCountFromJanrain import GetRecordsCountFromJanrain
from JanrainInternal.UpdateRecordsInJanrain import UpdateRecordsInJanrain

if __name__ == "__main__":

    """
    
    """

    ####################################### Global Settings #######################################################
    RecordsFilePath = 'records.csv'
    CredentialsFilePath = 'credentials.csv'

    ####################################### Get Records  Methods ####################################################
    GetRecordsObj = GetRecordsFromJanrain(CredentialsFilePath)
    GetRecordsObj.getCredentials()

    ####################################### Update Records Methods ##################################################
    UpdateRecordsObj = UpdateRecordsInJanrain(CredentialsFilePath)

    ####################################### Delete Records Methods ##################################################

