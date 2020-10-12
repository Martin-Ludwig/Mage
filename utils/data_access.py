import mongoengine

from utils.Secrets import Secrets


# todo: exception handling

def db_connect(db_name=None):
    """ Connects to MongoDB database

    - looks up **secrets/secrets.env** for:
    - DATABASE_NAME
    - DATABASE_HOST

    :param db_name: Optional database name

    see documentation: https://docs.mongoengine.org/guide/connecting.html
    """
    settings = Secrets()
    if db_name is None:
        db_name = settings.get("DATABASE_NAME")
    db_host = settings.get("DATABASE_HOST")
    mongoengine.connect(db_name, host=db_host)


def find(model, **kwargs):
    """ Searches for objects

    see documentation: https://docs.mongoengine.org/guide/querying.html#query-operators

    :param model: Class model
    :param kwargs: see docs
    :return: list of objects of type <model>
    """
    return model.objects(**kwargs)


def find_one(model, **kwargs):
    """ Searches for objects

    see documentation: https://docs.mongoengine.org/guide/querying.html#query-operators

    :param model: Class model
    :param kwargs: see docs
    :return: first object found
    """
    return find(model, **kwargs)[0]


def delete_first(model, **kwargs):
    """ Deletes first document found with the query

    see documentation: https://docs.mongoengine.org/guide/querying.html#query-operators

    :param model: Class
    :param kwargs: Query Operator
    :return: Number of deleted documents
    """
    return model.objects(**kwargs)[0].delete()


def delete_all(model, **kwargs):
    """ Deletes all documents found with the query operation

    see documentation: https://docs.mongoengine.org/guide/querying.html#query-operators

    :param model: Class
    :param kwargs: Query Operator
    :return: Number of deleted documents
    """
    return model.objects(**kwargs).delete()