import random

from persistence import Configuration
from persistence import DatabaseManager

from model import Offer
from model import Product
from model import Store

CONFIGURATION_PATH = '/home/diego/workspaces/pycharm/aprovechalo/etc/aprovechalo.conf'
STORES_NUM = 10
PRODUCTS_PER_STORE = 10

configuration = Configuration(CONFIGURATION_PATH)
dm = DatabaseManager(configuration.persistence)

dm.drop_schema()
dm.create_schema()


# Store creation
def virtual_creation():
    with dm.session_scope() as db:
        stores = []
        for i in range(STORES_NUM):
            store = Store(
                name="Tienda {}".format(i),
                latitude=0.0,
                longitude=0.0
            )
            offers = []
            for j in range(PRODUCTS_PER_STORE):
                pr = Product(
                    store=store,
                    name="Product {},{}".format(i, j),
                    img_url="http://www.lavozlibre.com/userfiles/2a_decada/image/FOTOS%202013/04%20ABRIL%202013/02%20ABRIL%202013/yogures.jpg",
                    price="3€"
                )
                offers.append(
                    Offer(
                        product=pr,
                        offer_price="2€",
                        store=store
                    )
                )
                store.products.append(pr)
            db.add_all(offers)
            stores.append(store)
        db.add_all(stores)


def more_real_creation():
    with dm.session_scope() as db:
        stores = [
            Store(
                name="DIA",
                latitude=41.6342682,
                longitude=-4.7174426
            ),
            Store(
                name="Lupa",
                latitude=41.6364703,
                longitude=-4.7300158
            ),
            Store(
                name="Sushitería Valladolid",
                latitude=41.652698,
                longitude=-4.7317036
            ),
            Store(
                name="La tienda del alérgico",
                latitude=41.6547928,
                longitude=-4.7303049
            ),
            Store(
                name="Pantaleón Muñoz",
                latitude=41.6530984,
                longitude=-4.7325059
            ),
        ]

        products_img = {
            'Pizza Jamón Queso': 'https://s1.dia.es/medias/hc7/h5a/8830828478494.png',
            'Yogur Griego': 'https://s2.dia.es/medias/hd5/ha3/8821838413854.png',
            'Menestra de verduras': 'https://s0.dia.es/medias/h76/h6e/8822061498398.png',
            'Brocoli, Coliflor y Zanahoria': 'https://s2.dia.es/medias/h56/haf/8823785324574.png',
            'Zumo de frutas': 'https://s1.dia.es/medias/h00/h56/8823862919198.png',
            'Muesli': 'https://s2.dia.es/medias/h91/hda/8823751376926.png',
            'Frutas reglero': 'https://s2.dia.es/medias/h79/ha3/8846882668574.png',
            'Huevos': 'https://s3.dia.es/medias/h8e/ha8/8822320496670.png',
            'Merluza del cabo': 'https://s1.dia.es/medias/hc6/ha4/8823008755742.png',
            'Filetes de panga empanados': 'https://s1.dia.es/medias/h01/hc0/8823923867678.png',
            'Rodaja de Merluza': 'https://s0.dia.es/medias/hc1/hc0/8833209761822.png',
            'Empanada de atún': 'https://stag-s2.dia.es/medias/h43/hc6/8823204511774.png',
            'Pimientos de piquillo': 'https://s0.dia.es/medias/hef/hbe/8822377250846.png',
            'Callos con garbanzos': 'https://s0.dia.es/medias/h92/he6/8823167680542.png',
            'Paté senior': 'https://s0.dia.es/medias/hde/h66/8828547629086.png',
            'Albóndigas Allinut de carne': 'https://s2.dia.es/medias/h3c/h63/8864079642654.jpg',
            'Chuletas de cordero (bolsa)': 'https://s3.dia.es/medias/h28/h2b/8846911569950.png',
            'Mozarella fresca': 'https://s-media-cache-ak0.pinimg.com/236x/78/9f/1d/789f1d665b51885f478de2990cbe2dd9.jpg',
            'Mantequilla Light': 'https://stag-s0.dia.es/medias/ha5/h7e/8830444404766.png',
            'Habas baby': 'https://s0.dia.es/medias/h5e/h6f/8823714021406.png',
            'Plátano maduro': 'http://cdn0.hoy.com.do/wp-content/uploads/2014/08/PLATANO.jpg',
        }
        offers = []
        for name, url in products_img.items():
            stores[0].products.append(
                Product(
                    store=stores[0],
                    name=name,
                    img_url=url,
                    price="3€"
                )
            )
            offers.append(
                Offer(
                    product=stores[0].products[-1],
                    offer_price="2€",
                    store=stores[0]
                )
            )
        db.add_all(stores)
        db.add_all(offers)

if __name__ == "__main__":
    # virtual_creation()
    more_real_creation()
