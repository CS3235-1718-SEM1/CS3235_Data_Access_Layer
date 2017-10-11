from setuptools import setup

setup(
    name='dal',
    packages=['dal'],
    include_package_data=True,
    install_requires=[
        'flask',
        'psycopg2',
        'sqlalchemy',
        'flask-sqlalchemy'
    ]
)
