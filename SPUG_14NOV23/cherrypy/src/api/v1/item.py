import cherrypy

from core.lib.items import remove
from core.lib.item import get, update


@cherrypy.expose
@cherrypy.popargs("item")
class Item:
    exposed = True
    @cherrypy.tools.json_out()
    def GET(self, item):
        return {
            "self": f"https://api.spokanepython.com/cherrypy/item/{item}",
            "item": get(item)
        }

    def PATCH(self, item, **kwargs):
        update(item, kwargs)
        cherrypy.response.status = 204


    def DELETE(self, item):
        remove(item)
        cherrypy.response.status = 204
