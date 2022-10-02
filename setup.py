from setuptools import setup, find_packages

VERSION = "0.1"
DESCRIPTION = "ecoledirecteapi est une librairie python permetant de communiquer simplement avec l'api ecole directe"
    
setup(
    name='ecoledirecteapi',
    version=VERSION,
    license='MIT',
    author="Borane#9999",
    packages=[
        "ecoledirecteapi"
    ],
    url='https://github.com/8borane8/ecoledirecteapi',
    keywords='ecole directe api',
    python_requires='>=3.6',
    description=DESCRIPTION,
    install_requires=[
          'requests'
    ]
)