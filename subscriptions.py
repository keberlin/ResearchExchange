from dataclasses import dataclass


@dataclass
class Subscription:
    user: int
    book: int


class Subscriptions:
    def __init__(self):
        # Initialise a blank list of subscriptions
        self.subscriptions = []

    def create_new_subscription(self, user, book):
        subs = Subscription(user, book)
        self.subscriptions.append(subs)
        return subs

    def find_by_user(self, user):
        ret = []
        for subs in self.subscriptions:
            if subs.user == user:
                ret.append(subs)
        return ret

    def delete_subscriptions(self, subs):
        for sub in subs:
            self.subscriptions.remove(sub)
