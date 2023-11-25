from distutils.core import setup

setup(
    name='Picsort',
    version='1.0',
    description='Sorting image based on features',
    author='Rodenas Alexandre',
    packages=['src'],
    entry_points={
        'console_scripts': [
            'sort = src.main:run',
        ],
    },
)
