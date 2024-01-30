import grpc
import inventory_pb2
import inventory_pb2_grpc


def AddProduct(stub):
    product = inventory_pb2.Product(
        productIdentifier = 1,
        productName = "2",
        productQuantity = 3,
        productPrice = 4.0
    )

def GetAllProducts(stub):
    response_iterator = stub.GetAllProducts(inventory_pb2.Empty())
    for i in response_iterator:
        print("Product:", i)

    response = stub.AddProduct(i)

    print("AddProduct response:", response.status)

def UpdateProductQuantity(stub, productID, quantity):

    request = inventory_pb2.Quantity(
        productIdentifier = productID,
        productQuantity = quantity
    )

    response = stub.UpdateProductQuantity(request)
    print("UpdateProductQuantity:", response)

def GetProductById(stub, productID):

    productIdentifier = inventory_pb2.ProductIdentifier(productIdentifier=productID)
    response = stub.GetProductById(productIdentifier)

    if response.productIdentifier:
        print("GetProductById:", response)
    else:
        print("Product not found")


def DeleteProduct(stub, productID):
    productIdentifier = inventory_pb2.ProductIdentifier(productIdentifier=productID)
    response = stub.DeleteProduct(productIdentifier)
    print("DeleteProduct:", response.status)



def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = inventory_pb2_grpc.InventoryServiceStub(channel)

    response = stub.AddProduct(inventory_pb2.Product(productIdentifier=1, productName="Example", productQuantity=10, productPrice=20.0))
    print("AddProduct:", response.status)

if __name__ == '__main__':
    run()
