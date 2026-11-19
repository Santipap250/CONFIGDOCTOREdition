#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
OBIXConfig Doctor — FPV Drone Configuration Analyzer
Setup & installation configuration
"""

from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='configdoctor',
    version='5.2.0',
    description='FPV Drone Configuration Analyzer & Optimization Tool',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='SanTiPapHacker',
    author_email='',
    url='https://github.com/Santipap250/CONFIGDOCTOREdition',
    license='Proprietary - All Rights Reserved',
    packages=find_packages(),
    python_requires='>=3.11',
    install_requires=[
        'Flask==3.1.3',
        'Werkzeug==3.1.9',
        'Jinja2>=3.1.6,<4.0',
        'python-dotenv==1.2.4',
        'Flask-WTF==1.3.0',
        'Flask-Limiter==4.1.1',
        'Flask-Compress==1.26',
        'psycopg[binary]>=3.3.9,<4.0',
    ],
    extras_require={
        # NOTE: pytest-flask intentionally excluded — it imports
        # `flask._request_ctx_stack`, removed in Flask 3.x, which crashes
        # pytest at collection time. tests/conftest.py defines its own
        # app/client fixtures, so nothing here depends on it.
        'dev': [
            'pytest>=7.4.0',
            'pytest-cov>=4.1.0',
            'pytest-mock>=3.11.1',
            'black>=23.7.0',
            'flake8>=6.0.0',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Flask',
        'Intended Audience :: End Users/Desktop',
        'Natural Language :: Thai',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Topic :: Internet :: WWW/HTTP',
    ],
    keywords='fpv drone config pid tuning analyzer',
)
