from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Float

from persistence import Base


class Product(Base):
    __tablename__ = 'product'

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(256))
    store_id = Column(Integer,
                      ForeignKey('store.id',
                                 onupdate='CASCADE',
                                 ondelete='CASCADE'))
    store = relationship('Store', lazy="subquery")
    price = Column(String(256))
    img_url = Column(String(256))

    def serialize(self, store=True):
        serial_product = {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "imgUrl": self.img_url,
        }
        if store:
            serial_product.update({
                "store": self.store.serialize(products=False),
            })

        return serial_product


class Store(Base):
    __tablename__ = 'store'

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(256))
    latitude = Column(Float)
    longitude = Column(Float)
    products = relationship('Product')

    def serialize(self, products=True, store=False):
        serial_store = {
            "id": self.id,
            "name": self.name,
            "location": {
                "latitude": self.latitude,
                "longitude": self.longitude
            }
        }

        if products:
            serial_store.update({
                "products": [pr.serialize(store=False) for pr in self.products]
            })

        if store:
            serial_store = {'store': serial_store}
        return serial_store


class Offer(Base):
    __tablename__ = 'offer'

    id = Column(Integer, autoincrement=True, primary_key=True)
    store_id = Column(Integer, ForeignKey('store.id', onupdate='CASCADE',
                                          ondelete='CASCADE'))
    store = relationship('Store', lazy="subquery")
    product_id = Column(Integer, ForeignKey('product.id', onupdate='CASCADE',
                                            ondelete='CASCADE'))
    product = relationship('Product', lazy="subquery")
    when = Column(DateTime,
                  default=datetime.utcnow,
                  nullable=False)
    offer_price = Column(String(4096))

    def serialize(self, store=True, product=True):
        serial_offer = {
            "id": self.id,
            "offerPrice": self.offer_price,
            "when": (self.when - datetime(1970, 1, 1)).total_seconds()
        }
        if product:
            serial_offer.update({
                "product": self.product.serialize(store=False),
            })

        if store:
            serial_offer.update({
                "store": self.store.serialize(products=False),
            })
        return serial_offer

