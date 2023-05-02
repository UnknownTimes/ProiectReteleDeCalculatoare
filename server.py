# Framework Twisted
# ==========================================================

from twisted.web import server, resource
from twisted.internet import reactor, endpoints


class HomePage(resource.Resource):
    isLeaf = True

    def render_GET(self, request):
        request.setHeader(b"content-type", b"text/plain")
        return b"Hello, World!"

endpoints.serverFromString(reactor, "tcp:8888").listen(server.Site(HomePage()))
print("Serverul ruleaza...")
reactor.run()
