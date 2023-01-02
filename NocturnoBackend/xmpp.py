import asyncio
import base64

from xml.dom import minidom

class WebSocket:
    def __init__(self, port):
        self.port = port
        print("XMPP started listening on port", port)

    def on(self, event, callback):
        if event == "connection":
            asyncio.get_event_loop().create_task(callback())
        elif event == "error":
            print("XMPP FAILED to start.")

class XMLBuilder:
    @staticmethod
    def create(element_name):
        return Element(element_name)

class Element:
    def __init__(self, element_name):
        self.name = element_name
        self.attributes = {}
        self.elements = []

    def attribute(self, name, value):
        self.attributes[name] = value
        return self

    def element(self, name, content=None):
        element = Element(name)
        if content is not None:
            element.content = content
        self.elements.append(element)
        return element

    def up(self):
        return self

    def tostring(self):
        xml = f"<{self.name}"
        for name, value in self.attributes.items():
            xml += f" {name}='{value}'"
        xml += ">"
        if hasattr(self, "content"):
            xml += self.content
        for element in self.elements:
            xml += element.tostring()
        xml += f"</{self.name}>"
        return xml

class XMLParser:
    @staticmethod
    def parse(xml_string):
        return minidom.parseString(xml_string)

def MakeID():
    return "some-id"

def DecodeBase64(data):
    return base64.b64decode(data)

global Clients
Clients = []

wss = WebSocket(port=80)

async def on_connection():
    ws = WebSocketConnection()
    accountId = ""
    jid = ""
    id = ""
    ID = MakeID()
    Authenticated = False

    async def on_message(message):
        if isinstance(message, bytes):
            message = message.decode()
        msg = XMLParser.parse(message)
        if not msg.documentElement:
            return Error(ws)

        if msg.documentElement.tagName == "open":
            open_element = XMLBuilder.create("open")
            open_element.attribute("xmlns", "urn:ietf:params:xml:ns:xmpp-framing")
            open_element.attribute("from", "prod.ol.epicgames.com")
            open_element.attribute("id", ID)
            open_element.attribute("version", "1.0")
            open_element.attribute("xml:lang", "en")
            ws.send(open_element.tostring())

            if Authenticated:
                stream_features_element = XMLBuilder.create("stream:features")
                stream_features_element.attribute("xmlns:stream", "http://etherx.jabber.org/streams")
                ver_element = stream_features_element.element("ver")
                ver_element.attribute("xmlns", "urn:xmpp:features:rosterver")
                starttls_element = stream_features_element.element("starttls")
                starttls_element.attribute("xmlns", "urn:ietf:params:xml:ns:xmpp-tls")
                bind_element = stream_features_element.element("bind")
                bind_element.attribute("xmlns", "urn:ietf:params:xml:ns:xmpp-bind")
                compression_element = stream_features_element.element("compression")
                compression_element.attribute("xmlns", "http://jabber.org/features/compress")
                compression_element.element("method", "zlib")
                session_element = stream_features_element.element("session")
                session_element.attribute("xmlns", "urn:ietf:params:xml:ns:xmpp-session")
                ws.send(stream_features_element.tostring())
                
            else:
                stream_features_element = XMLBuilder.create("stream:features")
                stream_features_element.attribute("xmlns:stream", "http://etherx.jabber.org/streams")
                mechanisms_element = stream_features_element.element("mechanisms")
                mechanisms_element.attribute("xmlns", "urn:ietf:params:xml:ns:xmpp-sasl")
                mechanisms_element.element("mechanism", "PLAIN")
                ver_element = stream_features_element.element("ver")
                ver_element.attribute("xmlns", "urn:xmpp:features:rosterver")
                starttls_element = stream_features_element.element("starttls")
                starttls_element.attribute("xmlns", "urn:ietf:params:xml:ns:xmpp-tls")
                compression_element = stream_features_element.element("compression")
                compression_element.attribute("xmlns", "http://jabber.org/features/compress")
                compression_element.element("method", "zlib")
                auth_element = stream_features_element.element("auth")
                auth_element.attribute("xmlns", "http://jabber.org/features/iq-auth")
                ws.send(stream_features_element.tostring())
                
        elif msg.documentElement.tagName == "auth":
            if not msg.documentElement.firstChild or not msg.documentElement.firstChild.nodeValue:
                return Error(ws)
            if not DecodeBase64(msg.documentElement.firstChild.nodeValue):
                return Error(ws)
            if not DecodeBase64(msg.documentElement.firstChild.nodeValue).split("\x00")[0]:
                return Error(ws)
            decoded_base64 = DecodeBase64(msg.documentElement.firstChild.nodeValue).split("\x00")
            if decoded_base64 and accountId and len(decoded_base64) == 3:
                Authenticated = True
                success_element = XMLBuilder.create("success")
                success_element.attribute("xmlns", "urn:ietf:params:xml:ns:xmpp-sasl")
                ws.send(success_element.tostring())
                Clients.append(ws)
            else:
                Error(ws)
                
        elif msg.documentElement.tagName == "starttls":
            proceed_element = XMLBuilder.create("proceed")
            proceed_element.attribute("xmlns", "urn:ietf:params:xml:ns:xmpp-tls")
            ws.send(proceed_element.tostring())
            
        elif msg.documentElement.tagName == "bind":
            bind_element = XMLBuilder.create("bind")
            bind_element.attribute("xmlns", "urn:ietf:params:xml:ns:xmpp-bind")
            resource_element = bind_element.element("resource")
            resource_element.content = "xiff"
            iq_element = XMLBuilder.create("iq")
            iq_element.attribute("id", msg.documentElement.getAttribute("id"))
            iq_element.attribute("type", "result")
            iq_element.appendChild(bind_element)
            ws.send(iq_element.tostring())
            
        elif msg.documentElement.tagName == "iq":
            if msg.documentElement.getAttribute("type") == "set":
                query_element = msg.documentElement.getElementsByTagName("query")[0]
                if query_element.getAttribute("xmlns") == "jabber:iq:roster":
                    iq_element = XMLBuilder.create("iq")
                    iq_element.attribute("id", msg.documentElement.getAttribute("id"))
                    iq_element.attribute("type", "result")
                    iq_element.attribute("to", msg.documentElement.getAttribute("from"))
                    query_element = iq_element.element("query")
                    query_element.attribute("xmlns", "jabber:iq:roster")
                    item_element = query_element.element("item")
                    item_element.attribute("jid", "nocturno@prod.ol.epicgames.com")
                    item_element.attribute("subscription", "both")
                    item_element.attribute("name", "NocturnoServer")
                    item_element.element("group", "Nocturno")
                    ws.send(iq_element.tostring())
                    
        elif msg.documentElement.tagName == "presence":
            presence_element = XMLBuilder.create("presence")
            presence_element.attribute("from", "nocturno@prod.ol.epicgames.com/xiff")
            presence_element.attribute("to", msg.documentElement.getAttribute("from"))
            presence_element.attribute("type", "subscribed")
            ws.send(presence_element.tostring())
            presence_element = XMLBuilder.create("presence")
            presence_element.attribute("from", "nocturno@prod.ol.epicgames.com/xiff")
            presence_element.attribute("to", msg.documentElement.getAttribute("from"))
            ws.send(presence_element.tostring())
        elif msg.documentElement.tagName == "close":
            ws.send("</stream:stream>")
        else:
            Error(ws)

    ws.on("message", on_message)

class WebSocketConnection:
    def send(self, data):
        print(f"Sending data: {data}")

    def on(self, event, callback):
        if event == "message":
            asyncio.get_event_loop().create_task(callback("some message"))

def Error(ws):
    error_element = XMLBuilder.create("error")
    error_element.attribute("type", "modify")
    error_element.attribute("code", "400")
    error_element.attribute("customCode", "0")
    error_element.attribute("xmlns", "jabber:client")
    error_element.element("bad-request")
    error_element.attribute("xmlns", "urn:ietf:params:xml:ns:xmpp-stanzas")
    ws.send(error_element.tostring())
    
asyncio.get_event_loop().run_until_complete(wss)
asyncio.get_event_loop().run_forever()