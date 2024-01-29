import grpc
import inventory_pb2
import inventory_pb2_grpc


def AddProduct(stub):
    product = inventory_pb2.Product(
        productIdentifier = 1,
        product_name = "2",
        product_quantity = 3,
        product_price = 4.0
    )

def GetAllProducts(stub):
    response_iterator = stub.GetAllProducts(inventory_pb2.Empty())
    for product in response_iterator:
        print("Product:", product)
    response = stub.AddProduct(product)
    print("AddProduct response:", response.status)

def UpdateProductQuantity(stub, productID, quantity):

    request = inventory_pb2.Quantity(
        productIdentifier = productID,
        product_quantity = quantity
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

    response = stub.AddProduct(inventory_pb2.Product(productIdentifier=1, product_name="Example", product_quantity=10, product_price=20.0))
    print("AddProduct:", response.status)

if __name__ == '__main__':
    run()
