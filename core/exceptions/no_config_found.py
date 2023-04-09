class NoConfigFound(Exception):
    def __str__(self):
        return 'No config file found.'
