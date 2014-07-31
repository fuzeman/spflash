from flask import Flask, Response, abort, request, render_template
import os

app = Flask(__name__, template_folder='../templates', static_folder='../static')
hostname = os.environ.get('HOSTNAME', 'localhost:5455')
drivers = {}

try:
    from pyvirtualdisplay import Display

    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    display = Display()
    display.start()
except ImportError:
    pass


@app.route('/<version>/get')
def get(version):
    ping = request.args.get('ping')

    if not ping:
        abort(400)

    driver = get_driver(version)
    print "Using driver: %s" % driver

    result = driver.execute_script("return document.getElementById('SPFBIn_2072_player').sp_run(arguments[0])", ping)
    print 'result: "%s"' % result

    return Response(result, mimetype='text/plain')


@app.route('/<version>/host')
def host(version):
    return render_template('host.html', version=version)


def get_driver(version):
    if version not in drivers:
        print "Constructing driver..."
        drivers[version] = webdriver.PhantomJS()

        print "Loading host page..."
        drivers[version].get("http://%s/%s/host" % (hostname, version))

        print "Waiting for page to finish loading..."
        WebDriverWait(drivers[version], 10).until(EC.presence_of_element_located((By.ID, "SPFBIn_2072_player")))

    return drivers[version]
