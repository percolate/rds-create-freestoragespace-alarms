from setuptools import setup


setup(
    name='rds-create-freestoragespace-alarms',
    version='1.4',
    description='AWS Cloudwatch RDS Tool for creating Metric Alarms',
    url='https://github.com/percolate/rds-create-freestoragespace-alarms',
    author='Mihailo Pavlisin',
    author_email='mihailo@percolate.com',
    license='GPLv3',
    keywords='aws rds2 rds alarms cloudwatch boto',
    packages=['rds_create_freestoragespace_alarms'],
    install_requires=[
        'boto',
        'docopt'
    ],
    entry_points={
        'console_scripts': [
            ('rds-create-freestoragespace-alarms='
             'rds_create_freestoragespace_alarms.main:main')
        ]
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Topic :: System :: Systems Administration"
    ]
)
