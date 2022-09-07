class Login():
    def __init__(self, title, url, username, password):
        self.title = title
        self.url = url
        self.username = username
        self.password = password

    def addBeforeActions(self, actions: list):
        self.beforeActions = actions

    def addBetweenActions(self, actions: list):
        self.betweenActions = actions

    def addAfterActions(self, actions: list):
        self.afterActions = actions
