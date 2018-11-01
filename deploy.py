from spyne import Application, rpc, ServiceBase, Iterable, Integer, Unicode
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication

import xml.etree.ElementTree as et

class HelloWorldService(ServiceBase):
    @rpc(Unicode, Integer, _returns=Iterable(Unicode))
    def say_hello(ctx, name, times):
        """Docstrings for service methods appear as documentation in the wsdl.
        <b>What fun!</b>
        @param name the name to say hello to
        @param times the number of times to say hello
        @return the completed array
        """

        for i in range(times):
            yield u'Hello, %s' % name;

class GetHobbyService(ServiceBase):
	#test 2 my hobby
	@rpc(_returns=Iterable(Unicode))
	def get_hobby(f):
		f = open("static\hobby.xml","r");
		print (f);
		return f;
		
class ParcelService(ServiceBase):
	@rpc(Unicode, Unicode, Unicode , Integer, Integer, _returns=Iterable(Unicode))
	def send_parcel_data(ctx, sname, rname, location, weight, status="0"):
		#file = open("static\data.txt", "w");
		file_path = "static\parceldata.xml";
		tree = et.parse(file_path);
		root = tree.getroot();
		allid = root.findall("id");
		lastid = allid[len(allid)-1].text;
		new_parcel = et.SubElement(root,"id");
		new_sender = et.SubElement(new_parcel,"sender");
		new_receiver = et.SubElement(new_parcel,"receiver");
		new_location = et.SubElement(new_parcel,"location");
		new_weight = et.SubElement(new_parcel,"weight");
		new_status = et.SubElement(new_parcel,"status");
		
		
		if (lastid == None) :
		    lastid = 0;
		    new_parcel.text = str(int(lastid)+1);
		else:
		    new_parcel.text = str(int(lastid)+1);
		new_sender.text = str(sname);
		new_receiver.text = str(rname);
		new_location.text = str(location);
		new_weight.text = str(weight);
		new_status.text = "On Shiping";
		tree.write(file_path);
		
		#file = open("static\parceldata.xml","w");
		#file.write('<parceldata>');
		#file.write('<sender>'+ str(sname) +'</sender>');
		#file.write('<receiver>' + str(rname) + '</receiver>');
		#file.write('<location>' + str(location)+'</location>');
		#file.write('<weight>'+str(weight)+'</weight>');
		#file.write('<status>'+str(status)+'</status>');
		#file.write('</parceldata>');
		#file.close();
		
		return [u'Save done!!'];
	
class GetParcelStatusService(ServiceBase):
	@rpc(Integer,_returns=Iterable(Unicode))
	def get_parcel_status(ctx,idn):
	    file_path = "static\parceldata.xml";
	    tree = et.parse(file_path);
	    root = tree.getroot();
	    elm = root.findall("id");
	    stat = ".";
	    for i in elm:
	        if(str(idn) == i.text):
	            stat = str(i.find("status").text);
	    return [stat];


class ChangeParcelStatusService(ServiceBase):
	@rpc(Unicode,Integer,_returns=Iterable(Unicode))
	def change_parcel_status(ctx,status,idn):
		file_path = "static\parceldata.xml";
		tree = et.parse(file_path);
		root = tree.getroot();
		elm = root.findall("id");
		stat = status;
		#print(str(type(status)) + " IDN is here");
		for i in elm:
		    #print(i.find("status").text);
		    if(str(idn) == i.text):
		        i.find("status").text = str(status);
		#print("If in" + str(i.find("status").text));
		#else:
		#print("Else in");
		tree.write(file_path);
		return [u'Change done!'];
	


application = Application([HelloWorldService, GetHobbyService ,ParcelService ,GetParcelStatusService,ChangeParcelStatusService], 'spyne.examples.hello.soap',
                          in_protocol=Soap11(validator='lxml'),
                          out_protocol=Soap11())

wsgi_application = WsgiApplication(application)


if __name__ == '__main__':
    import logging

    from wsgiref.simple_server import make_server

    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('spyne.protocol.xml').setLevel(logging.DEBUG)

    logging.info("listening to http://127.0.0.1:8000")
    logging.info("wsdl is at: http://localhost:8000/?wsdl")

    server = make_server('127.0.0.1', 8000, wsgi_application)
    server.serve_forever()