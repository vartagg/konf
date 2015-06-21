import os
from setuptools import setup, find_packages

version = "1.1.5"

description = (
    'Konf is a Python package which designed to simplify the use of variables in configuration files. '
    'json and yaml supported out of the box. '
)


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

long_description = read('README.rst')

install_requires=['PyYAML', 'good']


setup(
    name='konf',
    author="Vladimir Chub",
    author_email="vartagg@users.noreply.github.com",
    url='http://github.com/vartagg/konf/',
    description=description,
    long_description=long_description,
    keywords="konf,json,yaml,config",
    license="BSD",
    version=version,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3'
    ],
    packages=find_packages(),
    package_data = {'': ['testing/assets/*.json', 'testing/assets/*.yml']},
    install_requires=install_requires,
    tests_require=['nose'],
    test_suite='nose.collector',
    entry_points={},
)
