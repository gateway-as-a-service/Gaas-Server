import time

import cherrypy

import api.server
from api.configs.config import SERVER_PORT, SERVER_HOST

if __name__ == '__main__':
    cherrypy.tree.graft(api.server.app.wsgi_app, "/")
    cherrypy.config.update({
        "server.socket_host": SERVER_HOST,
        "server.socket_port": SERVER_PORT,
        "engine.autoreload.on": False,
        "server.thread_pool": 50,
    })
    cherrypy.server.subscribe()
    cherrypy.engine.start()

    api.server.app.logger.info("Server has started")

    while True:
        try:
            time.sleep(2)
        except KeyboardInterrupt:
            break
