import random
from datetime import datetime
from datetime import timedelta

from persistence import Configuration
from persistence import DatabaseManager

from model import Offer
from model import Product
from model import Store

CONFIGURATION_PATH = './etc/aprovechalo.conf'
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
        products_dia_img = {
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
        products_common_img = {
            'Pizza muy rica': 'https://image.freepik.com/foto-gratis/muy-rica-pizza_2536312.jpg',
            'Manzana': 'https://mejorconsalud.com/wp-content/uploads/2014/06/manzanas.jpg',
            'Pan': 'https://www.hogarmania.com/archivos/201203/pan-beneficios-salud-668x400x80xX.jpg',
            'Kiwi': 'http://www.healthline.com/hlcmsresource/images/topic_centers/Food-Nutrition/642x361_IMAGE_1_The_7_Best_Things_About_Kiwis.jpg',
            'Lechuga': 'http://biotrendies.com/wp-content/uploads/2015/07/lechuga.jpg',
            'Canónigos': 'http://www.esdemercado.com/images/thumbs/0002995_300.jpeg',
            'Entrecot': 'http://www.recetasparainutiles.com/sites/www.recetasparainutiles.com/files/8349.jpg?1348222298',
            'Chorizo': 'http://www.vegajardin.es/456-thickbox/chorizo-sarta.jpg',
            'Bacalao poco fresco': 'http://www.ecestaticos.com/image/clipping/654/bac6dfb5ecb9d9938151fa81146df205/los-filetes-de-bacalao-salado-suelen-ser-mas-grandes-que-los-que-se-encuentran-frescos-istock.jpg',
            'Naranjas': 'http://biotrendies.com/wp-content/uploads/2015/07/Naranja1.jpg',
            'Almejas': 'https://t1.uc.ltmcdn.com/images/4/5/5/img_como_conservar_almejas_frescas_25554_600.jpg',
            'Oreja': 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/85/Orejas_de_cerdo_-_Cerca.jpg/300px-Orejas_de_cerdo_-_Cerca.jpg',
            'Callos': 'http://www.paxinasgalegas.es/fiestas/imagenes/xxiv-festa-dos-callos-salceda-de-caselas_img197n3t0.jpg',
            'Atún': 'https://www.ocu.org/-/media/ocu/images/home/alimentacion/alimentos/tests/comparar-atun/500x281_atun.jpg?h=-1&w=-1&la=es-ES&hash=5CEBB1E55D8D95B999CFEE1B17C460915B4A5EFE',
            'Cordero': 'http://www.comycebaleares.com/galeria/menus/A_carne_cordero_red.jpg',
            'Lomo de cerdo': 'http://burruezocongelados.es/imagenes/productos/301016.jpg',
            'Jamón york': 'http://www.abc.es/Media/201401/24/jamon-york--478x270.jpg',
            'Queso Fresco': 'http://www.gourmetsleuth.com/images/default-source/dictionary/queso-fresco.jpg?sfvrsn=6',
            'Chopped': 'http://www.embutidoslaseca.com/comprar/UserFiles/Image/up/314.JPG',
            'Pechuga de pavo': 'https://consejonutricion.files.wordpress.com/2012/07/pechuga_de_pavo.jpg',
            'Pechuga de pollo': 'https://consejonutricion.files.wordpress.com/2012/07/pechuga_de_pavo.jpg',
        }
        products_tuples = []

        for name, url in products_common_img.items():
            products_tuples.append((name, url))

        offers = []
        for name, url in products_dia_img.items():
            price = round(random.choice(range(20, 30)) / 10.0, 2)
            stores[0].products.append(
                Product(
                    store=stores[0],
                    name=name,
                    img_url=url,
                    price="{}€".format(price)
                )
            )
            offers.append(
                Offer(
                    product=stores[0].products[-1],
                    offer_price="{}€".format(round(price - price * 0.3, 2)),
                    store=stores[0]
                )
            )
        for store in stores[1:]:
            for n in range(1, 20):
                pr = random.choice(products_tuples)
                price = round(random.choice(range(20, 30)) / 10.0, 2)
                store.products.append(
                    Product(
                        store=store,
                        name=pr[0],
                        img_url=pr[1],
                        price="{}€".format(price)
                    )
                )
                offers.append(
                    Offer(
                        product=store.products[-1],
                        offer_price="{}€".format(round(price - price * 0.3, 2)),
                        store=store,
                        when=datetime.now() - timedelta(minutes=random.choice(range(10, 20)))
                    )
                )

        db.add_all(stores)
        db.add_all(offers)

if __name__ == "__main__":
    # virtual_creation()
    more_real_creation()
