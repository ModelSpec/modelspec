# %% NEW FILE FriendRequest BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 29 "model.ump"
# line 102 "model.ump"

class FriendRequest():
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #FriendRequest Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aSender, aReceiver):
        self._receiver = None
        self._sender = None
        didAddSender = self.setSender(aSender)
        if not didAddSender :
            raise RuntimeError ("Unable to create senderOf due to sender. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")
        didAddReceiver = self.setReceiver(aReceiver)
        if not didAddReceiver :
            raise RuntimeError ("Unable to create receiverOf due to receiver. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")

    #------------------------
    # INTERFACE
    #------------------------
    # Code from template association_GetOne 
    def getSender(self):
        return self._sender

    # Code from template association_GetOne 
    def getReceiver(self):
        return self._receiver

    # Code from template association_SetOneToMany 
    def setSender(self, aSender):
        wasSet = False
        if aSender is None :
            return wasSet
        existingSender = self._sender
        self._sender = aSender
        if not (existingSender is None) and not existingSender == aSender :
            existingSender.removeSenderOf(self)
        self._sender.addSenderOf(self)
        wasSet = True
        return wasSet

    # Code from template association_SetOneToMany 
    def setReceiver(self, aReceiver):
        wasSet = False
        if aReceiver is None :
            return wasSet
        existingReceiver = self._receiver
        self._receiver = aReceiver
        if not (existingReceiver is None) and not existingReceiver == aReceiver :
            existingReceiver.removeReceiverOf(self)
        self._receiver.addReceiverOf(self)
        wasSet = True
        return wasSet

    def delete(self):
        placeholderSender = self._sender
        self._sender = None
        if not (placeholderSender is None) :
            placeholderSender.removeSenderOf(self)
        placeholderReceiver = self._receiver
        self._receiver = None
        if not (placeholderReceiver is None) :
            placeholderReceiver.removeReceiverOf(self)
