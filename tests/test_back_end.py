class TestBase(TestCase):

    def create_app(self):

        # pass in configurations for test database
        config_name = 'testing'
        app.config.update(TEST_DATABASE_URI=getenv('mysql+pymysql://root:root@35.246.125.7/testdb'),
                          TEST_SECRET_KEY=getenv('smtb98'),
                          WTF_CSRF_ENABLED=False,
                          DEBUG=True
                          )
        return app
