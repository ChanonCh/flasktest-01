from suds.client import Client

#client = Client('https://flasktest-01.herokuapp.com/?wsdl', cache=None)
client = Client('http://localhost:8000/?wsdl', cache=None)

#print(client.service.say_hello(u'J?r?me', 5));
d = client.service.get_hobby();
#print(type(d));
#file = open("data.xml", "w");
#for i in range(len(d)):
	#file.write(d[i]+'');
#;
#file.close();
print(d);
