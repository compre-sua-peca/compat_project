class DSPConfig:
    DSP_GATEWAY_URL = 'http://gateway:5000'


class Config(DSPConfig):
    DEBUG = True
    DEVELOPMENT = True
    TESTING = False