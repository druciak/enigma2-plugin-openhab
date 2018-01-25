# -*- coding: UTF-8 -*-

from . import debug

from zope.interface import implements

from twisted.internet import reactor
from twisted.internet.defer import Deferred, succeed
from twisted.internet.protocol import Protocol
from twisted.web.client import HTTPConnectionPool, Agent, ResponseDone
from twisted.web.http_headers import Headers
from twisted.web.iweb import IBodyProducer
import base64
from json import loads as json_loads


class StringProducer(object):
    implements(IBodyProducer)

    def __init__(self, body):
        self.body = body
        self.length = len(body)

    def startProducing(self, consumer):
        consumer.write(self.body)
        return succeed(None)

    def pauseProducing(self):
        pass

    def stopProducing(self):
        pass

class JsonReceiver(Protocol):
    
    def __init__(self, onFinish):
        self.onConnLost = onFinish

    def connectionMade(self):
        debug("Started receiving data")
        self.data = ""

    def dataReceived(self, data):
        debug("Received data chunk: %d" % len(data))
        self.data += data

    def connectionLost(self, reason):
        debug("Receiving stopped, reason: %s" % str(reason))
        if reason.check(ResponseDone):
            debug("All data received, total size: %d" % len(self.data))
            try:
                self.onConnLost.callback(json_loads(self.data))
            except ValueError, e:
                self.onConnLost.errback(e)
        else:
            self.onConnLost.errback(reason)

class RestClient(object):
    
    def __init__(self, host, port, username, password):
        self.url = "http://{}:{}/rest/".format(host, port)
        self.pool = HTTPConnectionPool(reactor, persistent=True)
        self.agent = Agent(reactor, pool=self.pool)
        self.std_headers = {
                           "Content-type": ["text/plain"],
                           "Accept": ["application/json"],
                           "Cache-Control": ["max-age=0"]
                           }
        if username and password:
            auth = base64.encodestring("{}:{}".format(username, password)).replace("\n", "")
            self.std_headers["Authorization"] = ["Basic " + auth]
    
    def make_req(self, url, method="GET", data=None):

        def on_response(response):
            debug("Response received, code: %d" % response.code)
            if response.code == 200:
                response.deliverBody(JsonReceiver(result))
            else:
                result.errback(response)
            return result

        def on_error(err):
            result.errback(err)
            return result

        debug("Making %s request to %s" % (method, url))
        result = Deferred()
        post = data is not None
        deferred = self.agent.request(method, url, Headers(self.std_headers), StringProducer(data) if post else None)
        deferred.addCallback(on_response)
        deferred.addErrback(on_error)
        return result
    
    def get_sitemap(self, name):
        url = self.url + "sitemaps/" + name
        return self.make_req(url)
    
    def get_state(self, name):
        url = self.url + "items/" + name
        return self.make_req(url)

    def set_state(self, name, state):
        url = self.url + "items/" + name
        return self.make_req(url, "PUT", state)

    def send_cmd(self, name, cmd):
        url = self.url + "items/" + name
        return self.make_req(url, "POST", cmd)
    

###########################################################################

def main():
    def refresh_data(data):
        print data
    def on_error(err):
        print "Error!!!", err
    
    ri = RestClient("192.168.1.1", 8080)
    d = ri.get_sitemap("demo")
    d.addCallback(refresh_data)
    d.addErrback(on_error)
    d.addBoth(lambda ign: reactor.callWhenRunning(reactor.stop))
    reactor.run()

if __name__ == "__main__":
    main()
