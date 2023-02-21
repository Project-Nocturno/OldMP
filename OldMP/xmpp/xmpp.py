import socket
from threading import Thread
from uuid import uuid4
from datetime import datetime
import base64
import random

from modules.SocketSession import Session as sessions

class Xmpp():
    def __init__(self, port: int=3556, sessionL: dict={}):
        self.port=port
        self.sessionL=sessionL

    def find(self, list, arg):
        for i in list:
            for z in i:
                if z==arg:
                    return i
        return None
    
    def genId(self):
        letters="AZERTYUIOPQSDFGHJKLMWXCVBNazertyuiopqsdfghjklmwxcvbn1234567890"
        id=''.join(random.choice(letters) for i in range(10))
        return id

    def send(self, socket, data: str="", auto: bool=True):
        if auto:
            if not '<?xml' in data:
                maindata=data.split('</stream:features>')[0]
                maindata+='<c xmlns="http://jabber.org/protocol/caps" hash="sha-1" node="https://www.igniterealtime.org/projects/openfire/" ver="GfhZeaVxkWh61dF2uCv3iGcaCko="/>'
                data=maindata+"</stream:features>"+data.split('</stream:features>')[1]
        socket.send(data.encode())
        print(f'\nSend: {data}')

    def error(self, socket):
        socket.send('')
        socket.close()

    def sendPresence(self, socket, body: dict={}):
        for jid in sessions(self.sessionL, socket).list('jid'):
            data=f'<presence corr-id="{sessions(self.sessionL, socket).found(jid)["corrid"]}" from="{jid}" to="{sessions(self.sessionL, socket).get("jid")}">'
            data+=f'<delay xmlns="urn:xmpp:delay" stamp="{datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")}"></delay>'
            data+='<priority>0</priority>'
            data+=f'<status>{body}</status>'
            data+='</presence>'
            self.send(socket, data, False)

    def main(self):
        sock=socket.socket()
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            sock.bind(('0.0.0.0', self.port))
        except:
            print('Failed to bind port')
            exit()
        
        sock.listen(200)
        
        while 1:
            Thread(target=self.handle_client, args=[*sock.accept()]).start()    
    
    def handle_client(self, client, address):
        
        print(f'\nNew client: {address}')
        
        if not sessions(self.sessionL, client).exist():
            sessions(self.sessionL, client).put('accountId', '')
            sessions(self.sessionL, client).put('jid', '')
            sessions(self.sessionL, client).put('id', self.genId())
            sessions(self.sessionL, client).put('ID', uuid4())
            sessions(self.sessionL, client).put('auth', False)
            sessions(self.sessionL, client).put('tls', False)
        else:
            pass
                
        data=client.recv(1024).decode()
        
        if not data:
            pass
        
        print(f'\nRecieve: {data}')
        msg=[i.split('=') for i in data.replace('/>', '').replace('</', '').replace('<', '').replace('>', '').replace('"', '').replace("'", '').split(' ')]
        
        key=msg[0][0]
        print(f'\n{key}')
        if key=='stream:stream':
            if not sessions(self.sessionL, client).get('auth'):
                if not sessions(self.sessionL, client).get('tls'):
                    self.send(client, f'''<?xml version='1.0' encoding='UTF-8'?><stream:stream xmlns:stream="http://etherx.jabber.org/streams" xmlns="jabber:client" from="127.0.0.1" id="{sessions(self.sessionL, client).get("id")}" xml:lang="und" version="1.0">''')
                    self.send(client, '<stream:features><starttls xmlns="urn:ietf:params:xml:ns:xmpp-tls"></starttls><mechanisms xmlns="urn:ietf:params:xml:ns:xmpp-sasl"><mechanism>PLAIN</mechanism></mechanisms><compression xmlns="http://jabber.org/features/compress"><method>zlib</method></compression></stream:features>')
                else:
                    self.send(client, f'''<?xml version='1.0' encoding='UTF-8'?><stream:stream xmlns:stream="http://etherx.jabber.org/streams" xmlns="jabber:client" from="127.0.0.1" id="{sessions(self.sessionL, client).get("id")}" xml:lang="und" version="1.0"><stream:features><mechanisms xmlns="urn:ietf:params:xml:ns:xmpp-sasl"><mechanism>PLAIN</mechanism></mechanisms><compression xmlns="http://jabber.org/features/compress"><method>zlib</method></compression><ver xmlns="urn:xmpp:features:rosterver"/></stream:features>ÖyéZÖyéZÖyéZÖyéZÖyéZ''')
            else:
                self.send(client, f'''<success xmlns="urn:ietf:params:xml:ns:xmpp-sasl"/>am xmlns:stream="http://etherx.jabber.org/streams" xmlns="jabber:client" from="127.0.0.1" id="{sessions(self.sessionL, client).get("id")}" xml:lang="und" version="1.0"><stream:features><mechanisms xmlns="urn:ietf:params:xml:ns:xmpp-sasl"><mechanism>PLAIN</mechanism></mechanisms><compression xmlns="http://jabber.org/features/compress"><method>zlib</method></compression><ver xmlns="urn:xmpp:features:rosterver"/></stream:features>ÖyéZÖyéZÖyéZÖyéZÖyéZ''')
                self.send(client, f'''<?xml version='1.0' encoding='UTF-8'?><stream:stream xmlns:stream="http://etherx.jabber.org/streams" xmlns="jabber:client" from="127.0.0.1" id="{sessions(self.sessionL, client).get("id")}" xml:lang="und" version="1.0"><stream:features><compression xmlns="http://jabber.org/features/compress"><method>zlib</method></compression><ver xmlns="urn:xmpp:features:rosterver"/><bind xmlns="urn:ietf:params:xml:ns:xmpp-bind"/><session xmlns="urn:ietf:params:xml:ns:xmpp-session"><optional/></session></stream:features>á2·¤¦Df♀9ïs◄''')
        
        elif key=='starttls':
            self.send(client, '<proceed xmlns="urn:ietf:params:xml:ns:xmpp-tls"/>xml:ns:xmpp-tls"><mechanisms xmlns="urn:ietf:params:xml:ns:xmpp-sasl"><mechanism>PLAIN</mechanism></mechanisms><compression xmlns="http://jabber.org/features/compress"><method>zlib</method></compression><ver xmlns="urn:xmpp:features:rosterver"/></stream:features>')
            sessions(self.sessionL, client).put('tls', True)
            
        elif key=='auth':
            if not sessions(self.sessionL, client).get('auth'):
                datas=self.find(msg, 'xmlns:auth')
                datas=base64.b64decode(datas[1].replace('http://www.google.com/talk/protocol/auth', ''))
                token=datas.split('NOCTURNOISBETTER_')[1]
                username=datas.split('NOCTURNOISBETTER_')[0]
                sessions(self.sessionL, client).put('token', token)
                sessions(self.sessionL, client).put('accountId', username)
                
                self.send(client, f'''<?xml version='1.0' encoding='UTF-8'?><stream:stream xmlns:stream="http://etherx.jabber.org/streams" xmlns="jabber:client" from="127.0.0.1" id="{sessions(self.sessionL, client).get("id")}" xml:lang="und" version="1.0"><stream:features><mechanisms xmlns="urn:ietf:params:xml:ns:xmpp-sasl"><mechanism>PLAIN</mechanism></mechanisms><compression xmlns="http://jabber.org/features/compress"><method>zlib</method></compression><ver xmlns="urn:xmpp:features:rosterver"/></stream:features>ÖyéZÖyéZÖyéZÖyéZÖyéZ''')
                self.send(client, f'''<success xmlns="urn:ietf:params:xml:ns:xmpp-sasl"/>am xmlns:stream="http://etherx.jabber.org/streams" xmlns="jabber:client" from="127.0.0.1" id="{sessions(self.sessionL, client).get("id")}" xml:lang="und" version="1.0"><stream:features><mechanisms xmlns="urn:ietf:params:xml:ns:xmpp-sasl"><mechanism>PLAIN</mechanism></mechanisms><compression xmlns="http://jabber.org/features/compress"><method>zlib</method></compression><ver xmlns="urn:xmpp:features:rosterver"/></stream:features>ÖyéZÖyéZÖyéZÖyéZÖyéZ''')
                sessions(self.sessionL, client).put('auth', True)
                
            else:
                pass
            
        elif key=='iq':
            id=self.find(msg, 'id')[1]
            type=self.find(msg, 'type')[1]
            
            if id=='6': # resource
                if type=='set':
                    sessions(self.sessionL, client).put('resource', self.find(msg, 'xmlns')[1].split('resource')[1])
                    sessions(self.sessionL, client).put('jid', f'{sessions(self.sessionL, client).get("username")}@oldmp.software/{sessions(self.sessionL, client).get("resource")}')
                    self.send(client, f'''<?xml version='1.0' encoding='UTF-8'?><stream:stream xmlns:stream="http://etherx.jabber.org/streams" xmlns="jabber:client" from="127.0.0.1" id="{sessions(self.sessionL, client).get("id")}" xml:lang="und" version="1.0"><stream:features><compression xmlns="http://jabber.org/features/compress"><method>zlib</method></compression><ver xmlns="urn:xmpp:features:rosterver"/><bind xmlns="urn:ietf:params:xml:ns:xmpp-bind"/><session xmlns="urn:ietf:params:xml:ns:xmpp-session"><optional/></session></stream:features>á2·¤¦Df♀9ïs◄''')
                    self.send(client, f'''<iq type="result" id="{id}" to="127.0.0.1/{sessions(self.sessionL, client).get("id")}"><bind xmlns="urn:ietf:params:xml:ns:xmpp-bind"><jid>{sessions(self.sessionL, client).get("jid")}</jid></bind></iq><stream:features><compression xmlns="http://jabber.org/features/compress"><method>zlib</method></compression><ver xmlns="urn:xmpp:features:rosterver"/><bind xmlns="urn:ietf:params:xml:ns:xmpp-bind"/><session xmlns="urn:ietf:params:xml:ns:xmpp-session"><optional/></session></stream:features>á2·¤¦Df♀9ïs◄''')
            
            elif id=='7': # session
                if type=='set':
                    self.send(client, f'''<iq type="result" id="6" to="127.0.0.1/{sessions(self.sessionL, client).get("id")}"><bind xmlns="urn:ietf:params:xml:ns:xmpp-bind"><jid>{sessions(self.sessionL, client).get("jid")}</jid></bind></iq><stream:features><compression xmlns="http://jabber.org/features/compress"><method>zlib</method></compression><ver xmlns="urn:xmpp:features:rosterver"/><bind xmlns="urn:ietf:params:xml:ns:xmpp-bind"/><session xmlns="urn:ietf:params:xml:ns:xmpp-session"><optional/></session></stream:features>á2·¤¦Df♀9ïs◄''')
                    self.send(client, f'''<iq type="result" id="7" from="{sessions(self.sessionL, client).get("username")}@oldmp.software" to="{sessions(self.sessionL, client).get("jid")}"/>{sessions(self.sessionL, client).get("resource")}</jid></bind></iq><stream:features><compression xmlns="http://jabber.org/features/compress"><method>zlib</method></compression><ver xmlns="urn:xmpp:features:rosterver"/><bind xmlns="urn:ietf:params:xml:ns:xmpp-bind"/><session xmlns="urn:ietf:params:xml:ns:xmpp-session"><optional/></session></stream:features>á2·¤¦Df♀9ïs◄''')
                
            elif id=='8': # ping
                if type=='get':
                    pass
                
        elif key=='presence':
            corrid=self.find(msg, 'corr-id')[1].split('status')[0]
            status=self.find(msg, 'corr-id')[1].split('status')[1]
            sessions(self.sessionL, client).put('corrid', corrid)
            sessions(self.sessionL, client).put('status', status)
            
            if status['Properties']==[]:
            
                self.send(client, f'''<iq type="result" id="7" from="{sessions(self.sessionL, client).get("username")}@oldmp.software" to="{sessions(self.sessionL, client).get("jid")}"/>{sessions(self.sessionL, client).get("resource")}</jid></bind></iq><stream:features><compression xmlns="http://jabber.org/features/compress"><method>zlib</method></compression><ver xmlns="urn:xmpp:features:rosterver"/><bind xmlns="urn:ietf:params:xml:ns:xmpp-bind"/><session xmlns="urn:ietf:params:xml:ns:xmpp-session"><optional/></session></stream:features>á2·¤¦Df♀9ïs◄''')
                self.send(client, f'''<iq type="result" id="8" from="{sessions(self.sessionL, client).get("username")}@oldmp.software" to="{sessions(self.sessionL, client).get("jid")}"/>{sessions(self.sessionL, client).get("resource")}</jid></bind></iq><stream:features><compression xmlns="http://jabber.org/features/compress"><method>zlib</method></compression><ver xmlns="urn:xmpp:features:rosterver"/><bind xmlns="urn:ietf:params:xml:ns:xmpp-bind"/><session xmlns="urn:ietf:params:xml:ns:xmpp-session"><optional/></session></stream:features>á2·¤¦Df♀9ïs◄''')
                self.send(client, f'''<iq type="result" id="8" from="{sessions(self.sessionL, client).get("username")}@oldmp.software" to="{sessions(self.sessionL, client).get("jid")}"/>{sessions(self.sessionL, client).get("resource")}</jid></bind></iq><stream:features><compression xmlns="http://jabber.org/features/compress"><method>zlib</method></compression><ver xmlns="urn:xmpp:features:rosterver"/><bind xmlns="urn:ietf:params:xml:ns:xmpp-bind"/><session xmlns="urn:ietf:params:xml:ns:xmpp-session"><optional/></session></stream:features>á2·¤¦Df♀9ïs◄''')
                self.send(client, f'''<presence corr-id="{corrid}" from="{sessions(self.sessionL, client).get("username")}@oldmp.software" to="{sessions(self.sessionL, client).get("jid")}"><status>{status}</status><priority>0</priority><delay xmlns="urn:xmpp:delay" stamp="{datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")}"></delay></presence><optional/></session></stream:features>á2·¤¦Df♀9ïs◄''')
            
            elif status['Properties'][0]['Name']=='FortBasicInfo': #list all users ?
                self.sendPresence(client, status)


Xmpp(3556, {}).main()