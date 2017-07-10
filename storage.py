import os
import pickle

PICKLE_FOLDER = '{}/storage'.format(os.path.abspath(os.path.dirname(__file__)))


def create_pickle_folder(func):
    def return_func(*args, **kwargs):
        try:
            os.mkdir(PICKLE_FOLDER)
        except FileExistsError:
            pass
        return func(*args, **kwargs)
    return return_func


@create_pickle_folder
def pickle_object(target, name):
    """Pickle object target under name."""

    with open('storage/{}'.format(name), 'wb') as jar:
        pickle.dump(target, jar)


@create_pickle_folder
def unpickle_object(name):
    """Return unpickled object of name."""
    with open('storage/{}'.format(name), 'rb') as jar:
        unpickled = pickle.load(jar)
    return unpickled
