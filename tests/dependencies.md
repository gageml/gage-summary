# Gage Summary Dependencies

The `gage-summaries` package must not have any install time
dependencies.

    >>> import tomli

    >>> config = tomli.load(open("pyproject.toml", "rb"))

    >>> config["project"]["dependencies"]
    []
