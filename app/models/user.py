class CurrentUser:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CurrentUser, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.user_id = None
        self.email = None
        self.name = None
        self.role = None
        self.is_authenticated = False

    def login(self, user_id, email, name, role):
        self.user_id = user_id
        self.email = email
        self.name = name
        self.role = role
        self.is_authenticated = True

    def logout(self):
        self.user_id = None
        self.email = None
        self.name = None
        self.role = None
        self.is_authenticated = False

    @property
    def is_logged_in(self):
        return self.is_authenticated
    
    def __str__(self):
        if self.is_authenticated:
            return f"Usuario: {self.name} ({self.email})"
        return "Usuario no autenticado"
