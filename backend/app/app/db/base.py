# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base  # noqa
from app.db_models.models import *  # noqa
# from app.db_models.item import Item  # noqa
