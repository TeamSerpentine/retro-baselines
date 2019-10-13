import os
import glob
import pyclbr
import importlib


def model_finder(game_mode):
    """ Returns an initialized model.

        :param game_mode: str
            Should be either the name of a module located in the
            models folder or the name of the first class inside one of the modules
            located in models.

            In case there are multiple classes inside a module, the first
            one will be selected.
    """

    # Go up to retro_baseline folder
    path_file = os.path.dirname(os.path.dirname(__file__))

    # Find all modules located in models library (non-recursive), unequal to base_model
    models = glob.glob(os.path.join(path_file, "models", "[!base_model]*.py"))

    # Extract module name
    models_name = [os.path.basename(each)[:-3] for each in models]

    # Locate all classes inside the module
    classes = [pyclbr.readmodule_ex("models." + name) for name in models_name]

    # Select the first class from the module
    classes_keys = [next(iter(k)) for k in classes]

    # Check for name as module
    if game_mode in models_name:
        # Get the name of the class that has to be imported
        to_import_class = classes_keys[models_name.index(game_mode)]

        # Import the module
        module = importlib.import_module(f"models.{game_mode}")

        # Return class instance
        return getattr(module, to_import_class)

    # Check for name as Class Name
    if game_mode in classes_keys:
        # Get the name of the module that has to be imported
        to_import_module = models_name[classes_keys.index(game_mode)]

        # Import the module
        module = importlib.import_module(f"models.{to_import_module}")

        # Return class instance
        return getattr(module, game_mode)
    else:
        # Combine the module name and first Class Name from that module and then
        # make a single string out of them with enters between them.
        valid = "\n  ".join([f'{k.ljust(25)}{v}' for (k, v) in zip(models_name, classes_keys)])
        print("\nUnrecognized model, valid inputs were:\n  "
              f"{valid}")
        exit(1)
