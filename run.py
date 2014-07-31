from spflash.controllers import app
import logging
import os

if __name__ == '__main__':
    debug = bool(os.environ.get('DEBUG', False))
    port = int(os.environ.get('PORT', 5455))

    if debug:
        logging.basicConfig(level=logging.DEBUG)

    app.run(host='0.0.0.0', port=port, debug=debug, threaded=True)
