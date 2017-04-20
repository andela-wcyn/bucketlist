from . import auth


@auth.route('/login', methods=['POST'])
def login():
    pass


@auth.route('/register', methods=['POST'])
def register():
    pass
