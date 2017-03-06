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
from setuptools import setup


_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('flask/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))


setup(
    name='Flask',
    version=version,
    url='https://github.com/yxwzaxns/cowry',
    license='MIT',
    author='aong',
    author_email='yxwzaxns@gmail.com',
    description='A Secure FTPS system',
    long_description=__doc__,
    packages=['cowry'],
    include_package_data=True,
    zip_safe=False,
    platforms='Linux,MacOS',
    install_requires=[
        'Werkzeug>=0.7',
        'Jinja2>=2.4',
        'itsdangerous>=0.21',
        'click>=2.0',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    entry_points='''

    '''
)
