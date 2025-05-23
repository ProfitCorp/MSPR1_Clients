from sqlalchemy.orm import Session
from models import CustomerDB, OrderDB, ProductDB
from schemas import Customer, Order, Product, OrderDetails

# GET: Récupérer tous les clients
def get_all_customers(db: Session):
    customers = db.query(CustomerDB).all()
    return [customerdb_to_schema(c) for c in customers]

# POST: Créer un client
def create_customer(db: Session, customer_data: Customer):
    db_customer = CustomerDB(
        id=customer_data.id,
        created_at=customer_data.createdAt,
        name=customer_data.name,
        username=customer_data.username,
        first_name=customer_data.firstName,
        last_name=customer_data.lastName,
        postal_code=customer_data.address.postalCode,
        city=customer_data.address.city,
        profile_first_name=customer_data.profile.firstName,
        profile_last_name=customer_data.profile.lastName,
        company_name=customer_data.company.companyName,
    )
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return customerdb_to_schema(db_customer)

# DELETE: Supprimer un client
def delete_customer(db: Session, customer_id: str):
    db_customer = db.query(CustomerDB).filter(CustomerDB.id == customer_id).first()
    if not db_customer:
        return None
    db.delete(db_customer)
    db.commit()
    return db_customer

# Conversion DB vers schéma Pydantic
def customerdb_to_schema(db_customer: CustomerDB) -> Customer:
    return Customer(
        createdAt=db_customer.created_at,
        name=db_customer.name,
        username=db_customer.username,
        firstName=db_customer.first_name,
        lastName=db_customer.last_name,
        address={"postalCode": db_customer.postal_code, "city": db_customer.city},
        profile={"firstName": db_customer.profile_first_name, "lastName": db_customer.profile_last_name},
        company={"companyName": db_customer.company_name},
        id=db_customer.id,
        orders=[
            Order(
                id=order.id,
                createdAt=order.created_at,
                customerId=order.customer_id,
                products=[
                    Product(
                        id=prod.id,
                        createdAt=prod.created_at,
                        name=prod.name,
                        details=OrderDetails(
                            price=prod.price,
                            description=prod.description,
                            color=prod.color
                        ),
                        stock=prod.stock,
                        orderId=prod.order_id
                    )
                    for prod in order.products
                ] if order.products else []
            )
            for order in db_customer.orders
        ]
    )

def update_customer(db: Session, customer_id: str, customer_data: Customer):
    db_customer = db.query(CustomerDB).filter(CustomerDB.id == customer_id).first()
    if not db_customer:
        return None

    db_customer.created_at = customer_data.createdAt
    db_customer.name = customer_data.name
    db_customer.username = customer_data.username
    db_customer.first_name = customer_data.firstName
    db_customer.last_name = customer_data.lastName
    db_customer.postal_code = customer_data.address.postalCode
    db_customer.city = customer_data.address.city
    db_customer.profile_first_name = customer_data.profile.firstName
    db_customer.profile_last_name = customer_data.profile.lastName
    db_customer.company_name = customer_data.company.companyName

    db.commit()
    db.refresh(db_customer)
    return customerdb_to_schema(db_customer)
