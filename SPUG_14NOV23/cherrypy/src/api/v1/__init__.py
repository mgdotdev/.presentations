import cherrypy

@cherrypy.expose
class API:
    def GET(self):
        return "Hello World!"
