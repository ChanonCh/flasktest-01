from suds.client import Client
import xml.etree.ElementTree as et
client = Client('https://flasktest-01.herokuapp.com/?wsdl', cache=None)
#client = Client('http://localhost:8000/?wsdl', cache=None)

#print(client.service.say_hello(u'J?r?me', 5));
a = client.service.get_hobby();
print(a);
b = client.service.send_parcel_data(u'Non',u'Palm',u'Mainroad',22);
print(b);
c = client.service.get_parcel_status(3);
print(c);
d = client.service.change_parcel_status(u'Delivered', 3);
print(d);
e = client.service.get_parcel_status(3);
print(e);
#print(type(d));
#file = open("data.xml", "w");
#for i in range(len(d)):
	#file.write(d[i]+'');
#;
#file.close();

#print(s);

