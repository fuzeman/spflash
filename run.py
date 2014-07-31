from spflash.controllers import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5455, debug=True, threaded=True)
