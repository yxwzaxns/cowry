"""
Cowry
-----
Cowry is a FTPS system

run it:
.. code:: bash
    $ pip install cowry
     * Running on http://localhost:2333/

"""
import re
import ast
from setuptools import setup, find_packages

setup(
    name='Cowry',
    version='0.1al',
    url='https://github.com/yxwzaxns/cowry',
    license='MIT',
    author='aong',
    author_email='yxwzaxns@gmail.com',
    description='A Secure FTPS system',
    long_description=__doc__,
    packages=find_packages(exclude=['client', 'server']),
    include_package_data=True,
    zip_safe=False,
    platforms='Linux,MacOS,Windows',
    install_requires=[
        'PyQt5'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5'
    ],
    keywords='FTPS',
    entry_points='''

    '''
)
