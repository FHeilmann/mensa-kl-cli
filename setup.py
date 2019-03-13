from setuptools import setup

setup(name='mensa-kl-cli',
      version='0.1',
      author='Florian Heilmann',
      install_requires=['colorama==0.3.9',
                        'Click==7.0',
                        'beautifulsoup4==4.7.1'],
      py_modules=['mensa'],
      entry_points='''
        [console_scripts]
        mensa-kl=mensa:mensa
      ''',
      zip_safe=False
     )
