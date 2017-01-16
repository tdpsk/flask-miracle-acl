from setuptools import setup, find_packages

requirements = [
    'Flask',
    'miracle-acl'
]

setup(
    name='flask-miracle-acl',
    version='0.2',
    description='A connecting layer between the Flask framework and Miracle ACL',
    author='Timo "tdpsk" Puschkasch',
    author_email='timo@puschkasch.com',
    url='https://github.com/tdpsk/flask-miracle-acl',
    license='BSD',
    packages=find_packages(exclude=['tests']),
    platforms='any',
    install_requires=requirements,
    classifiers=[
        'Framework :: Flask',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: BSD License'
    ],
    test_suite='nose.collector',
    tests_require=['nose']
)
