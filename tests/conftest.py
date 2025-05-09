from hypothesis import settings

settings.register_profile('S', max_examples=100)
settings.register_profile('M', max_examples=250)
settings.register_profile('L', max_examples=1000)
settings.register_profile('XL', max_examples=5000)
settings.register_profile('XXL', max_examples=10000)
settings.register_profile('3XL', max_examples=50000)
