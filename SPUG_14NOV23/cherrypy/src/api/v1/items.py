import cherrypy

from core.lib import items, item

@cherrypy.expose
class Items:

    @cherrypy.tools.json_out()
    def GET(self):
        return {
            "self": "https://api.spokanepython.com/cherrypy/items/",
            "items": [
                f"https://api.spokanepython.com/cherrypy/item/{i}"
                for i in items.get()
            ]
        }


    def POST(self, name=None, description=None, timestamp=None, done=False):
        items.add(item.new(name, description, timestamp, done))
        cherrypy.response.status = 201


    def DELETE(self):
        items.clear()
        cherrypy.response.status = 204

