class User:
    def __init__(self, name, upn, roles=None, **kwargs):
        self.name = name
        self.upn = (upn,)
        self.roles = roles if roles else []
