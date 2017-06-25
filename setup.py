"""
Cowry
-----
Cowry is a secure distributed file transfer and share system

"""
import codecs
from setuptools import setup, find_packages

version = '0.0.1'

with codecs.open('README.rst', encoding='utf-8') as f:
    long_description = f.read()

with open('requirements.txt') as f:
    reqs = f.read().splitlines()

setup(
    name="cowry",
    version=version,
    license='MIT',
    description="a secure distributed file transfer and share system",
    author='aong',
    author_email='yxwzaxns@gmail.com',
    url='https://github.com/yxwzaxns/cowry',
    packages=find_packages(exclude=['examples', 'tests', 'docs']),
    include_package_data=True,
    install_requires=reqs,
    entry_points="""
    [console_scripts]
    cowry_server = server.server:main
    cowry_client = client.client:main
    """,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: File Transfer Protocol (FTP)',
    ],
    long_description=long_description,
)
