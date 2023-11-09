import cherrypy

from .items import Items
from .item import Item

@cherrypy.expose
class API:

    item = Item()
    items = Items()

    @cherrypy.tools.json_out()
    def GET(self):
        return {
            "response": "this is the root of the cherrypy API"
        }
