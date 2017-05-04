class ErrorFormatter(object):
    @staticmethod
    def format_field_errors(errors):
        # Bad request
        return {"field_errors": errors}, 400

    @staticmethod
    def format_general_errors(errors):
        # Internal Server error
        return {"errors": errors}, 500
