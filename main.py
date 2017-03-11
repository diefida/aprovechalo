from flask import Flask, jsonify
from flask import request

from model import Store
from model import Offer

from persistence import Configuration
from persistence import DatabaseManager

CONFIGURATION_PATH = './etc/aprovechalo.conf'


configuration = Configuration(CONFIGURATION_PATH)
dm = DatabaseManager(configuration.persistence)

# dm.drop_schema()
# dm.create_schema()

app = Flask(__name__)


@app.route('/')
def index():
    return jsonify()


@app.route('/offers', methods=['GET'])
def get_offers():
    with dm.session_scope() as db:
        offers = db.query(Offer).all()
        reply = [o.serialize() for o in offers]

        return jsonify(reply)


@app.route('/products', methods=['GET'])
def get_products():
    store_id = request.args.get('store_id', None)
    offer_id = request.args.get('offer_id', None)

    if store_id and offer_id:
        store_id = int(store_id)
        offer_id = int(offer_id)
        with dm.session_scope() as db:
            store = db.query(Store).filter(Store.id == store_id).one()
            offer = db.query(Offer).filter(Offer.id == offer_id).one()
            pr = offer.product
            store.products.remove(pr)
            store.products = [pr] + store.products
            reply = store.serialize(store=True)

            reply['offer'] = offer.serialize(store=False, product=False)

            return jsonify(reply)
    else:
        return jsonify({

        })


@app.route('/stores', methods=['GET'])
def get_stores():
    with dm.session_scope() as db:
        stores = db.query(Store).all()
        reply = [s.serialize(products=False) for s in stores]

        return jsonify(reply)


if __name__ == '__main__':
    app.run(host=configuration.server['host'],
            port=configuration.server['port'],
            debug=configuration.server['debug'] == 'True')
