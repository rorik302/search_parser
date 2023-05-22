from setuptools import setup, find_packages

setup(
    name='search_parser',
    version='0.1',
    packages=find_packages(),
    py_modules=['engines', 'main'],
    description="Search engines parser",
    author='rorik302',
    author_email='rorik302@gmail.com',
    install_requires=[
        "beautifulsoup4==4.9.1",
        "requests==2.31.0",
    ],
    entry_points={
        'console_scripts': [
            'search = main:main',
        ]
    },
)
