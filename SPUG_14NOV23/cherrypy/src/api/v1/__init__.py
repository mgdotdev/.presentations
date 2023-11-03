import cherrypy


@cherrypy.expose
class API:

    @cherrypy.tools.json_out()
    def GET(self):
        return {
            "response": "this is the root of the cherrypy API"
        }
