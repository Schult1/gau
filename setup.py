"""Package setup.
"""
import os
from setuptools import find_packages, setup


version_file = os.path.join(os.path.dirname(__file__), 'version.py')
__version__ = open(version_file).read().split("'")[1].rstrip("'\n")
README = os.path.join(os.path.dirname(__file__), 'README.md')
long_description = open(README).read()
setup(
    name='geo_api_utils',
    version=__version__,
    description='gau - Geo API Utilities',
    long_description=long_description,
    author='Christoph Schultens',
    author_email='christoph@schultens-family.de',
    license='None',
    packages=find_packages(),
    install_requires=[
        'folium',
        'geojson',
        'numpy',
        'pandas',
        'requests',
        'shapely',
        'flask_restplus'
    ]#,
    #test_suite='tests',
    #setup_requires=['pytest-runner'],
    #tests_require=['pytest', 'pytest-cov', 'hypothesis', 'mock', 'moto']
)
