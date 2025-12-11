from whatsapp_webhook.domain.repositories import MessageRepository, UserRepository

class MessageRepositoryImpl(MessageRepository):
    def __init__(self):
        self.messages = []

    def save_message(self, message):
        self.messages.append(message)

    def get_messages(self):
        return self.messages

class UserRepositoryImpl(UserRepository):
    def __init__(self):
        self.users = {}

    def save_user(self, user):
        self.users[user.id] = user

    def get_user(self, user_id):
        return self.users.get(user_id)