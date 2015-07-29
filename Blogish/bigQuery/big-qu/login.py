import main

class OauthHandler(Handler):
    def get(self):
        self.render('oauth.html')