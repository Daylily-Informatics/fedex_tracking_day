from setuptools import setup, find_packages

setup(
    name='fedex_tracking_day',
    version='0.2.8',
    description='A Python library to intereact with the FedEx Tracking API',
    author='John Major',
    author_email='john@daylilyinformatics.com',
    url='https://github.com/Daylily-Informatics/fedex_tracking_day',
    packages=find_packages(),
    install_requires=[
        'yaml_config_day',
        'requests',
        'pytz',
    ],
    entry_points={
        'console_scripts': [
            'fedex_tracking_day = fedex_tracking_day.fedex_track:main', 
        ],
    },
)
