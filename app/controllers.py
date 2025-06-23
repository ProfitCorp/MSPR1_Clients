"""Controllers for customer management using SQLAlchemy ORM."""

from mq.publish import publish_user_update, publish_user_delete
from sqlalchemy.orm import Session
from models import CustomerDB, OrderDB, ProductDB
from schemas import Customer, Order, Product, OrderDetails
from auth.security import hash_password


def get_all_customers(db: Session):
    """Retrieve all customers from the database."""
    customers = db.query(CustomerDB).all()
    return [customerdb_to_schema(c) for c in customers]


def create_customer(db: Session, customer_data: Customer):
    db_customer = CustomerDB(
        # created_at=customer_data.createdAt,
        # name=customer_data.name,
        username=customer_data.username,
        password=hash_password(customer_data.password),
        firstname=customer_data.firstName,
        lastname=customer_data.lastName,
        street_number=customer_data.address.streetNumber,
        street=customer_data.address.street,
        postalcode=customer_data.address.postalCode,
        city=customer_data.address.city,
        # profile_first_name=customer_data.profile.firstName,
        # profile_last_name=customer_data.profile.lastName,
        company_name=customer_data.companyName,
    )
    db.add(db_customer)

    # Traitement des commandes si présentes
    for order in customer_data.orders or []:
        db_order = OrderDB(
            created_at=order.createdAt,
            customer_id=db_customer.id
        )
        db.add(db_order)

        # Traitement des produits pour chaque commande
        for product in order.products or []:
            db_product = ProductDB(
                created_at=product.createdAt,
                name=product.name,
                price=product.details.price,
                description=product.details.description,
                color=product.details.color,
                stock=product.stock,
                order_id=order.id
            )
            db.add(db_product)

    db.commit()
    db.refresh(db_customer)
    return customerdb_to_schema(db_customer)



def delete_customer(db: Session, customer_id: str):
    """Delete a customer from the database by ID."""
    db_customer = db.query(CustomerDB).filter(CustomerDB.id == customer_id).first()
    if not db_customer:
        return None
    db.delete(db_customer)
    db.commit()

    publish_user_delete(customer_id)
    return db_customer


def customerdb_to_schema(db_customer: CustomerDB) -> Customer:
    """Convert a CustomerDB instance to a Customer Pydantic model."""
    return Customer(
        id=db_customer.id,
        # createdAt=db_customer.created_at,
        # name=db_customer.name,
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
        # profile={
        #     "firstName": db_customer.profile_first_name,
        #     "lastName": db_customer.profile_last_name,
        # },
        companyName=db_customer.company_name,
        
        orders=[
            Order(
                id=order.id,
                createdAt=order.created_at,
                customerId=order.customer_id,
                products=(
                    [
                        Product(
                            id=prod.id,
                            createdAt=prod.created_at,
                            name=prod.name,
                            details=OrderDetails(
                                price=prod.price,
                                description=prod.description,
                                color=prod.color,
                            ),
                            stock=prod.stock,
                            orderId=prod.order_id,
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

    # Mettre à jour les champs simples
    # db_customer.created_at = customer_data.createdAt
    # db_customer.name = customer_data.name
    db_customer.username = customer_data.username
    db_customer.password = customer_data.password
    db_customer.firstname = customer_data.firstName
    db_customer.lastname = customer_data.lastName
    db_customer.street_number = customer_data.address.streetNumber
    db_customer.street_number = customer_data.address.street
    db_customer.postalcode = customer_data.address.postalCode
    db_customer.city = customer_data.address.city
    # db_customer.profile_first_name = customer_data.profile.firstName
    # db_customer.profile_last_name = customer_data.profile.lastName
    db_customer.company_name = customer_data.companyName

    # Supprimer les anciennes commandes (et produits via cascade)
    for order in db_customer.orders:
        db.delete(order)

    # Ajouter les nouvelles commandes
    for order_data in customer_data.orders or []:
        db_order = OrderDB(
            id=order_data.id,
            created_at=order_data.createdAt,
            customer_id=db_customer.id,
        )
        db.add(db_order)

        for product in order_data.products or []:
            db_product = ProductDB(
                id=product.id,
                created_at=product.createdAt,
                name=product.name,
                price=product.details.price,
                description=product.details.description,
                color=product.details.color,
                stock=product.stock,
                order_id=order_data.id,
            )
            db.add(db_product)

    db.commit()
    db.refresh(db_customer)

    publish_user_update(customer_id, customer_data.dict())
    return customerdb_to_schema(db_customer)
