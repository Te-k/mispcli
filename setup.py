from setuptools import setup

setup(
    name='mispcli',
    version='0.1.1',
    description='MISP CLI tool',
    url='https://github.com/Te-k/mispcli',
    author='Tek',
    author_email='tek@randhome.io',
    keywords='osint',
    include_package_data=True,
    install_requires=[
        'mispy',
        ],
    python_requires='>=3.5',
    license='GPLv3',
    packages=['mispcli', 'mispcli.commands'],
    package_dir={},
    package_data={},
    entry_points= {
        'console_scripts': [ 'misp=mispcli.main:main' ]
    }
)
