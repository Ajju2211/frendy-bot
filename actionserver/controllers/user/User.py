
# temporary STORAGE
CART = []
class User:
    def __init__(self):
        pass
    def appendToCart(self,senderId,data):
        CART.append({
            "id":id,
            "data":data
        })

    def getCurrentCart(self,senderId):
        """
        parameter: senderId
        returns: current unsaved Cart [{},{}] otherwise []
        """
        for cart in CART:
            if cart['id'] == senderId:
                return cart['data']

        else:
            return []
    def clearCurrentCart(self,senderId):
        """
        parameter: senderid
        returns: None (clears the cart)
        """
        for cart in CART:
            if cart['id'] == senderId:
                CART.remove(cart)
                
    def saveCart(self):
        """
        parameter: senderid
        returns: None (Save to database)
        """
        pass



        
