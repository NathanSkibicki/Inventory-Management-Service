import grpc
from concurrent import futures
import inventory_pb2_grpc
import inventory_pb2
import redis
import threading

class InventoryService(inventory_pb2_grpc.InventoryServiceServicer):

    def __init__(self):
        self.redis_client = redis.StrictRedis(host = 'localhost', port=6379, db= 0, decode_responses=True)

    #gets product information
    def _get_product_info(self, productIdentifier):
        with self.lock:
            productData = self.redis_client.hgetall(productIdentifier)
            if productData:
                return {
                    'productName': productData[b'productName'].decode(),
                    'productQuantity': int(productData[b'productQuantity'].decode()),
                    'productPrice': float(productData[b'productPrice'].decode())
                }
            else:
                return None
            
    #updates/sets the desired product
    def _set_product_info(self, productIdentifier, productName, productQuantity, productPrice):
        with self.lock:
            self.redis_client.hmset(productIdentifier, {
                'productName': productName,
                'productQuantity': productQuantity,
                'productPrice': productPrice
            })

    #Add product
    def AddProduct(self, request, context):
        productIdentifier = str(request.productIdentifier)
        productName = request.productName
        productQuantity = request.productQuantity
        productPrice = request.productPrice

        self._set_product_info(productIdentifier, productName, productQuantity, productPrice)

        return inventory_pb2.Status(status="Product Added")
    
    #Get ProductbyId
    def GetProductById(self, productIdentifier):

        productIdentifier = str(request.productIdentifier)
        #get product via Identifier
        productData = self._get_product_info(productIdentifier)

        if productData:
            return inventory_pb2.Product(
                productIdentifier = request.productIdentifier,
                productName =  productData['productName'],
                productQuantity = productData['productQuantity'],
                productPrice = productData['productPrice']
            )
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Product not found')
            return inventory_pb2.Product()
    
    #Update Products
    def UpdateProductQuantity(self, request, context):
        productData = self._get_product_info(str(request.productIdentifier))

        if productData:
            new_quantity = productData['productQuantity'] + request.productQuantity
            self._set_product_info(str(request.productIdentifier), productData['productName'], new_quantity, productData['productPrice'])
            return inventory_pb2.Product(
                 productQuantity = new_quantity,
                productIdentifier = request.productIdentifier,
                productName = productData['productName'],
                productPrice = productData['productPrice'],
            )
        
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Product not found')
            return inventory_pb2.Product()
    
    #Gets and lists all products
    def GetAllProducts(self, request, context):
        with self.lock:
            product_keys = self.redis_client.keys('*')
            for key in product_keys:
                productData = self._get_product_info(key.decode())
                yield inventory_pb2.Product(
                    productIdentifier=int(key),
                    productName=productData['productName'],
                    productQuantity=productData['productQuantity'],
                    productPrice=productData['productPrice']
                )

    #Deletes products from DB
    def DeleteProduct(self, request, context):
        with self.lock:
            result = self.redis_client.delete(request.productIdentifier)
            #if result exists
            if result != 1:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details('Product Does not exist')
                return inventory_pb2.Status()
            else:
                return inventory_pb2.Status(status="Product deleted")

    #Set server
    def serve():
        server= grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        inventory_pb2_grpc.add_InventoryServiceServicer_to_server(InventoryService(), server)
        server.add_insecure_port('[::]:50051')
        server.start()
        server.wait_for_termination()

    if __name__ == '__main__':
        serve()