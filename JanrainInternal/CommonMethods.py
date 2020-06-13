__author__ = "sats17"


class CommonMethods:

    @staticmethod
    def typeConverter(value):
        """
        Helper function convert integer to string
        :param value:
        :return:
        """
        if type(value) == int:
            return "\"" + str(value) + "\""
        else:
            return "\"" + value + "\""

