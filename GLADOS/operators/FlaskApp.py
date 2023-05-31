from website import create_app
import ssl
from Security_Camera.Security_Config import Configuration
app = create_app()
host='0.0.0.0'
port=8080

conf = Configuration()
if __name__ == '__main__':
    if conf.boolean('Connection','https'):
        
        #context.load_cert_chain(conf.get('Connection')['certificate'], conf.get('Connection')['key'])
        context = (r"C:\Users\MERT ÜNÜBOL\CYCLOP\GLADOS\operators\Security_Camera\server.pem",r"C:\Users\MERT ÜNÜBOL\CYCLOP\GLADOS\operators\Security_Camera\server.key")
        app.run(threaded=True, host=host,port=port,debug=False ,ssl_context = context)
    else:
        app.run(threaded=True, host=host,port=port,debug=True)
