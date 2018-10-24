from suds.client import Client

client = Client('https://flasktest-01.herokuapp.com/?wsdl', cache=None)

print(client.service.say_hello(u'J?r?me', 5))