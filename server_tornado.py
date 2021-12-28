# Make it run from the examples directory
import sys
sys.path.append("../liquer")
sys.path.append("../liquer-pcv")

from liquer import *
import liquer.ext.basic
import liquer.ext.meta
from liquer.recipes import RecipeSpecStore
import liquer.ext.lq_pandas # Add pandas support to liquer so that the dataframe conversions work
import liquer_pcv
from liquer.store import web_mount, mount, FileStore
from liquer.cache import set_cache, MemoryCache, FileCache
from liquer.state import set_var, get_vars
from liquer.pool import set_central_cache

from liquer.server.tornado_handlers import url_mapping, liquer_static_path
import tornado.ioloop
import tornado

import commands

web_mount("gui","dist/liquer/web/gui")
mount("data", RecipeSpecStore(FileStore("liquer-gui/examples/data")))
set_cache(MemoryCache())
url_prefix='/liquer'

class IndexHandler(tornado.web.RequestHandler):
    def prepare(self):
        header = "Content-Type"
        body = "text/html"
        self.set_header(header, body)
    def get(self):
        self.write(b"""<h1>Hello-world app</h1>
    <ul>
    <li><a href="/liquer/web/gui">GUI</a></li>
    <li><a href="/liquer/q/hello">just hello</a></li>
    <li><a href="/liquer/q/harmonic/harmonic.html">harmonic 100</a></li>
    </ul>
    """)


if __name__ == '__main__':
    url_prefix = "/liquer"
    port = 5000
    set_var("api_path", url_prefix + "/q/")
    set_var("server", f"http://localhost:{port}")
    set_central_cache(FileCache("cache"))

    application = tornado.web.Application(
        url_mapping() + [
            (
                r"/liquer/static/(.*)",
                tornado.web.StaticFileHandler,
                {"path": liquer_static_path()},
            ),
            (r"/", IndexHandler),
            (r"/index.html", IndexHandler),
        ]
    )
    application.listen(port)
    tornado.ioloop.IOLoop.current().start()
