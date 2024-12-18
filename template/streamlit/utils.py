from webapp.models import Sundae, Sale

def get_model_by_name(table_name):
    """Returns the SQLAlchemy model based on the table name."""
    if table_name.lower() == "sundaes":
        return Sundae
    elif table_name.lower() == "sales":
        return Sale
    else:
        return None
