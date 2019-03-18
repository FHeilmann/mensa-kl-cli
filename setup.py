import pathlib
import setuptools

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = HERE.joinpath("README.md").read_text()

setuptools.setup(name='mensa-kl-cli',
      version='0.1',
      author='Florian Heilmann',
      author_email='Florian.Heilmann@gmx.net',
      long_description=README,
      license="GPLv3",
      url="http://github.com/FHeilmann/mensa-kl-cli",
      long_description_content_type="text/markdown",
      install_requires=['Click==7.0',
                        'setuptools==20.7.0',
                        'halo==0.0.23',
                        'colorama==0.3.9',
                        'beautifulsoup4==4.7.1',
      ],
      py_modules=['mensa'],
      python_requires=">=3.5",
      entry_points={
          "console_scripts" : [
              "mensa-kl=mensa:mensa"
          ]
      },
      packages=setuptools.find_packages(),
      zip_safe=False,
      classifiers=[
          "Environment :: Console",
          "Development Status :: 3 - Alpha",
          "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
          "Operating System :: OS Independent",
          "Programming Language :: Python :: 3.5",
          "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
          ]
     )
