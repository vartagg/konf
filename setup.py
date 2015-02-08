import os
from setuptools import setup, find_packages
import pkg_resources

version = "1.1.2"

description = (
    'Konf is a Python package which designed to simplify the use of variables in configuration files. '
    'json and yaml supported out of the box. '
)


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

long_description = read('README.rst')


def package_installed(pkg):
    """Check if package is installed"""
    req = pkg_resources.Requirement.parse(pkg)
    try:
        pkg_resources.get_provider(req)
    except pkg_resources.DistributionNotFound:
        return False
    else:
        return True

install_requires=['PyYAML']

if package_installed('good'):
    install_requires.append('good')
elif package_installed('voluptuous'):
    install_requires.append('voluptuous')
else:
    install_requires.append('good')

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
