import os.path
from setuptools import setup, find_packages


def read_docs(filename):
    path = os.path.join(os.path.dirname(__file__), filename)
    return open(path).read()


setup(name='django-plugins',
      version='0.2.2',
      author='Mantas Zimnickas',
      author_email='sirexas@gmail.com',
      packages=find_packages(exclude=['sample-project']),
      install_requires=[
          'distribute',
          'django',
      ],
      url='https://bitbucket.org/sirex/django-plugins',
      download_url='http://pypi.python.org/pypi/django-plugins',
      license='LGPL',
      description='django-plugins.',
      long_description=read_docs('README.rst')+read_docs('CHANGES.rst'),
      include_package_data=True,
      exclude_package_data={'': ['sample-project']},
      zip_safe=False,
      classifiers = [
          'Development Status :: 5 - Production/Stable',
          'Environment :: Web Environment',
          'Framework :: Django',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ])
