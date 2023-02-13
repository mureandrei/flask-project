from ariadne import ObjectType, graphql_sync, load_schema_from_path, make_executable_schema, snake_case_fallback_resolvers
from ariadne.constants import PLAYGROUND_HTML
from flask import Flask, request, jsonify

from .gql_queries import resolve_create_customer, resolve_create_work_order, resolve_customer, resolve_customers, resolve_work_order, resolve_work_orders
from .db import db
from . import conf
from .models.enums.work_order_type import WorkOrderType
from .models.customer import Customer
from .models.work_order import WorkOrder

# graphql
query = ObjectType("Query")
query.set_field("customers", resolve_customers)
query.set_field("workOrders", resolve_work_orders)
query.set_field("customer", resolve_customer)
query.set_field("workOrder", resolve_work_order)
mutation = ObjectType("Mutation")
mutation.set_field("createCustomer", resolve_create_customer)
mutation.set_field("createWorkOrder", resolve_create_work_order)
type_defs = load_schema_from_path(conf.GRAPHQL_SCHEMA_PATH)
schema = make_executable_schema(
    type_defs, query, mutation, snake_case_fallback_resolvers
)

# setup flask app
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{conf.DB_FILE_PATH}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

# ensure all tables exist
with app.app_context():
    db.create_all()

@app.route("/graphql", methods=["GET"])
def graphql_playground():
    return PLAYGROUND_HTML, 200

@app.route("/graphql", methods=["POST"])
def graphql():
    data = request.get_json()
    success, result = graphql_sync(
        schema,
        data,
        context_value=request,
        debug=app.debug
    )

    status_code = 200 if success else 400
    return jsonify(result), status_code

@app.route("/test", methods=["POST"])
def omg():
    customer = Customer.query.get(1)
    work_order = WorkOrder(customer=customer.id, work_order_type="INSTALL", schedule="dwdwddw")
    db.session.add(work_order)
    db.session.commit()
    return work_order.to_dict()

if __name__ == "__main__":
    app.run(debug=True)
