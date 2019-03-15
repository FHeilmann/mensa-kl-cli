import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = HERE.joinpath("README.md").read_text()

setup(name='mensa-kl-cli',
      version='0.1',
      author='Florian Heilmann',
      author_email='Florian.Heilmann@gmx.net',
      long_description=README,
      license="GPLv3",
      url="http://github.com/FHeilmann/mensa-kl-cli",
      long_description_content_type="text/markdown",
      install_requires=['colorama==0.3.9',
                        'Click==7.0',
                        'beautifulsoup4==4.7.1'],
      py_modules=['mensa'],
      python_requires=">=3.5",
      entry_points={
          "console_scripts" : [
              "mensa-kl=mensa:mensa"
          ]
      },
      zip_safe=False
     )
