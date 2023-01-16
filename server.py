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
from liquer.store import web_mount, mount, FileStore, get_store
from liquer.cache import set_cache, MemoryCache
import commands

web_mount("gui","dist/liquer/web/gui")
mount("data", RecipeSpecStore(FileStore("liquer-gui/examples/data")))

### Create Flask app and register LiQuer blueprint
from flask import Flask
import liquer.server.blueprint as bp
app = Flask(__name__)

set_cache(MemoryCache())

url_prefix='/liquer'
app.register_blueprint(bp.app, url_prefix=url_prefix)


@app.route('/')
@app.route('/index.html')
def index():
    return """<h1>Hello-world app</h1>
    <ul>
    <li><a href="/liquer/web/gui">GUI</a></li>
    <li><a href="/liquer/q/hello">just hello</a></li>
    <li><a href="/liquer/q/harmonic/harmonic.html">harmonic 100</a></li>
    </ul>
    """


if __name__ == '__main__':
    query="data/hello.txt"
#    get_store().store_metadata(query, {"title":"test"})
#    print(get_store().get_metadata(query))
    app.run(debug=True)
