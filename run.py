from spflash.controllers import app
import logging
import os

if __name__ == '__main__':
    port = os.environ.get('PORT', 5455)

    logging.basicConfig(level=logging.DEBUG)
    app.run(host='0.0.0.0', port=int(port), debug=True, threaded=True)
