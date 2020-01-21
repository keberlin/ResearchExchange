from dataclasses import dataclass


@dataclass
class User:
    id: int
    email: str


class Users:
    def __init__(self):
        # Initialise a blank list of users
        self.users = []
        self.index = 1

    def create_new_user(self, email):
        user = User(self.index, email)
        self.users.append(user)
        self.index += 1
        return user

    def find_by_id(self, id):
        for user in self.users:
            if user.id == id:
                return user
        return None

    def find_by_email(self, email):
        for user in self.users:
            if user.email == email:
                return user
        return None

    def delete_user(self, user):
        self.users.remove(user)
