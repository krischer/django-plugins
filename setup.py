import os.path
from setuptools import setup, find_packages


def read_docs(filename):
    path = os.path.join(os.path.dirname(__file__), filename)
    return open(path).read()

long_description = \
"""``django-plugins`` provides functionality for Django apps to make them more reusable.


Home page
    http://pypi.python.org/pypi/django-plugins

Documentation
    http://packages.python.org/django-plugins/

Source code:
    https://github.com/krischer/django-plugins\n\n"""

long_description += read_docs('CHANGES.rst')

setup(name='django-plugins',
      version='0.2.4',
      author='Mantas Zimnickas',
      author_email='sirexas@gmail.com',
      packages=find_packages(exclude=['sample-project']),
      install_requires=[
          'django>=1.5',
      ],
      url='https://github.com/krischer/django-plugins',
      download_url='http://pypi.python.org/pypi/django-plugins',
      license='LGPL',
      description='django-plugins.',
      long_description=long_description,
      include_package_data=True,
      exclude_package_data={'': ['sample-project']},
      zip_safe=False,
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Web Environment',
          'Framework :: Django',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: '
          'GNU Library or Lesser General Public License (LGPL)',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ])
