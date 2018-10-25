from spyne import Application, rpc, ServiceBase, Iterable, Integer, Unicode

from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication


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
		print f;
		return f;
		
class ParcelService(ServiceBase):
	@rpc(Unicode, Unicode, Unicode , Integer, Integer, _returns=Iterable(Unicode))
	def send_parcel_data(ctx, sname, rname, location, weight, status=0):
		#file = open("static\data.txt", "w");
		file = open("static\parceldata.xml","w");
		file.write('<parceldata>');
		file.write('<sender>'+ str(sname) +'</sender>');
		file.write('<receiver>' + str(rname) + '</receiver>');
		file.write('<location>' + str(location)+'</location>');
		file.write('<weight>'+str(weight)+'</weight>');
		file.write('<status>'+str(status)+'</status>');
		file.write('</parceldata>');
		file.close();
		
		return [u'Save done!!'];
	
class GetParcelStatusService(ServiceBase):
	@rpc(_returns=Iterable(Unicode))
	def get_parcel_status(f):
		file = open("static\parceldata.xml", 'r');
		return file;
	


application = Application([HelloWorldService, GetHobbyService ,ParcelService ,GetParcelStatusService], 'spyne.examples.hello.soap',
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