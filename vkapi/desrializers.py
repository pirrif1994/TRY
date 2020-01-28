import io
from rest_framework.parsers import JSONParser

stream = io.BytesIO(json)
data = JSONParser().parse(stream)

serializer = ProfileSerializers(data=data)
serializer.is_valid()
serializer.valiated_data