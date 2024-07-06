def get_field_from_verbose(meta, verbose_name):
    """
    Retrieves the name of a field from the given model's meta information based on its verbose name.

    Args:
        meta (django.db.models.options.Options): The meta information of the model.
        verbose_name (str): The verbose name of the field.

    Returns:
        str: The name of the field.

    Raises:
        KeyError: If a field with the given verbose name is not found.
    """
    try:
        return next(f.name for f in meta.get_fields() if f.verbose_name == verbose_name)
    except:
        raise KeyError(verbose_name)