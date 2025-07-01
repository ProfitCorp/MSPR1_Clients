"""Controllers for customer management using SQLAlchemy ORM."""

from mq.publish import publish_user_update, publish_user_delete, publish_user_create
from sqlalchemy.orm import Session
from models import CustomerDB, OrderDB, ProductDB
from schemas import Customer, Order, Product, OrderDetails
from auth.security import hash_password
from logs.logger import setup_logger

logger = setup_logger()


def get_all_customers(db: Session, user_id=None, role="user"):
    if role == "admin":
        customers = db.query(CustomerDB).all()
    else:
        customers = db.query(CustomerDB).filter(CustomerDB.id == user_id).all()

    logger.debug(customers)
    return [customerdb_to_schema(c) for c in customers]


def create_customer(db: Session, customer_data: Customer):
    db_customer = CustomerDB(
        username=customer_data.username,
        password=hash_password(customer_data.password),
        firstname=customer_data.firstName,
        lastname=customer_data.lastName,
        street_number=customer_data.address.streetNumber,
        street=customer_data.address.street,
        postalcode=customer_data.address.postalCode,
        city=customer_data.address.city,
        company_name=customer_data.companyName,
    )
    db.add(db_customer)

    for order in customer_data.orders or []:
        db_order = OrderDB(
            customer_id=db_customer.id
        )
        db.add(db_order)

        for product in order.products or []:
            db_product = ProductDB(
                name=product.name,
                price=product.details.price,
                description=product.details.description,
                color=product.details.color,
                stock=product.stock,
                order_id=order.id
            )
            db.add(db_product)
    publish_user_create(customer_data.dict())
    db.commit()
    db.refresh(db_customer)
    logger.debug(customer_data)
    return customerdb_to_schema(db_customer)



def delete_customer(db: Session, customer_id: str):
    db_customer = db.query(CustomerDB).filter(CustomerDB.id == customer_id).first()
    if not db_customer:
        return None
    db.delete(db_customer)
    publish_user_delete(customer_id)
    db.commit()
    logger.debug(db_customer)
    return db_customer


def customerdb_to_schema(db_customer: CustomerDB) -> Customer:
    return Customer(
        id=db_customer.id,
        username=db_customer.username,
        password=db_customer.password,
        firstName=db_customer.firstname,
        lastName=db_customer.lastname,
        address={
            "streetNumber": db_customer.street_number,
            "street": db_customer.street,
            "postalCode": db_customer.postalcode, 
            "city": db_customer.city
        },
        companyName=db_customer.company_name,
        
        orders=[
            Order(
                id=order.id,
                customerId=order.customer_id,
                products=(
                    [
                        Product(
                            id=prod.id,
                            name=prod.name,
                            details=OrderDetails(
                                price=prod.price,
                                description=prod.description,
                                color=prod.color,
                            ),
                            stock=prod.stock
                        )
                        for prod in order.products
                    ]
                    if order.products
                    else []
                ),
            )
            for order in db_customer.orders
        ],
    )


def update_customer(db: Session, customer_id: str, customer_data: Customer):
    db_customer = db.query(CustomerDB).filter(CustomerDB.id == customer_id).first()
    if not db_customer:
        return None

    db_customer.username = customer_data.username
    db_customer.password = customer_data.password
    db_customer.firstname = customer_data.firstName
    db_customer.lastname = customer_data.lastName
    db_customer.street_number = customer_data.address.streetNumber
    db_customer.street_number = customer_data.address.street
    db_customer.postalcode = customer_data.address.postalCode
    db_customer.city = customer_data.address.city
    db_customer.company_name = customer_data.companyName

    for order in db_customer.orders:
        db.delete(order)

    for order_data in customer_data.orders or []:
        db_order = OrderDB(
            id=order_data.id,
            customer_id=db_customer.id,
        )
        db.add(db_order)

        for product in order_data.products or []:
            db_product = ProductDB(
                id=product.id,
                name=product.name,
                price=product.details.price,
                description=product.details.description,
                color=product.details.color,
                stock=product.stock,
                order_id=order_data.id,
            )
            db.add(db_product)
    publish_user_update(customer_id, customer_data.dict())
    db.commit()
    db.refresh(db_customer)
    logger.debug(db_customer)
    return customerdb_to_schema(db_customer)
