# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .models import Product
# from .serializers import ProductSerializer

# class ProductAPIView(APIView):
#     def get(self, request):
#         products = Product.objects.all()
#         serializer = ProductSerializer(products, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = ProductSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def put(self, request, pk):
#         try:
#             product = Product.objects.get(pk=pk)
#         except Product.DoesNotExist:
#             return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)
#         serializer = ProductSerializer(product, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk):
#         try:
#             product = Product.objects.get(pk=pk)
#         except Product.DoesNotExist:
#             return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)




from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import ProductService
import asyncio

class ProductAPIView(APIView):
    def get(self, request):
        service = ProductService()
        # Run the async method in a synchronous context
        products = asyncio.run(service.get_all_products())
        return Response(products, status=status.HTTP_200_OK)

    def post(self, request):
        result = asyncio.run(ProductService.create_product(request.data))
        if result.get("success"):
            return Response(result["data"], status=status.HTTP_201_CREATED)
        return Response(result["errors"], status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        result = asyncio.run(ProductService.update_product(pk, request.data))
        if result.get("success"):
            return Response(result["data"])
        return Response(result["errors"], status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        result = asyncio.run(ProductService.delete_product(pk))
        if result.get("success"):
            return Response({"message": result["message"]}, status=status.HTTP_204_NO_CONTENT)
        return Response({"error": result["message"]}, status=status.HTTP_404_NOT_FOUND)
