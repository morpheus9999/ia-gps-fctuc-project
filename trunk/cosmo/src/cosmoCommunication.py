class Communication:

	def __init__(self, communicationId, receivedStep, communicationType, message):

		self.__communicationId = communicationId
		self.__receivedStep = receivedStep
		self.__type = communicationType
		self.__message = message


	def __str__(self):

		return '[Communication ' + str(self.__communicationId) + ']' + \
			'\n\tReceivedStep: ' + str(self.__receivedStep) + \
			'\n\tType: ' + self.__type + \
			'\n\tMessage: ' + self.__message


	def getCommunicationId(self):

		return self.__communicationId


	def getReceivedStep(self):

		return self.__receivedStep


	def getType(self):

		return self.__type


	def getMessage(self):

		return self.__message
