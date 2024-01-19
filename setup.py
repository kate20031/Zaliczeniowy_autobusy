from setuptools import setup, find_packages

setup(
    name='BusTracker',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'requests',
        'beautifulsoup4',
        'pandas'
    ],

    python_requires='>=3.8',
    url = 'https://github.com/kate20031/Zaliczeniowy_autobusy.git',
)