from setuptools import setup, find_packages

setup(
    name='Synapse',
    verson='0.2',
    long_description=__doc__,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Flask',
        'MongoWrapper',
        'MongoEngine',
        'Markdown',
        'Unidecode'
        ]
    )
