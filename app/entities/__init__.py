class User:
    def __init__(self, id, email, password):
        self.id = id
        self.email = email
        self.password = password


class Todo:
    def __init__(self, id, title, txt, user_id, done):
        self.id = id
        self.title = title
        self.txt = txt
        self.user_id = user_id
        self.done = done
