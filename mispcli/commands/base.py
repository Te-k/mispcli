class Command(object):
    config = None # Describes the configuration params
    update_needed = False

    def add_arguments(self, parser):
        pass
