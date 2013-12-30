__author__ = 'Lars Djerf <lars.djerf@gmail.com'

from setuptools import setup

setup(name="rambler",
      version="0.1",
      description="",
      license="GPLv3",
      author="Lars Djerf",
      author_email="lars.djerf@gmail.com",
      url="http://github.com/sral/rambler",
      packages=["rambler"],
      entry_points={
            "console_scripts": ["rambler = rambler.rambler:main"]
        })