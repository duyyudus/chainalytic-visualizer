# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

# All dependences
deps = {
    'chainalytic_viz': [
        'ruamel.yaml',
        'jsonrpcserver',
        'jsonrpcclient[websockets]',
        'jsonrpcclient[requests]',
        'websockets',
        'aiohttp',
        'requests',
        'chainalytic @ git+https://github.com/duyyudus/chainalytic-framework#egg=chainalytic'
    ],
    'test': [
        'pytest',
    ],
    'dev': [
        'python-language-server',
        'tox',
        'pylint',
        'autopep8',
        'rope',
        'black',
    ]
}
deps['dev'] = (
    deps['chainalytic_viz'] +
    deps['dev']
)
deps['test'] = (
    deps['chainalytic_viz'] +
    deps['test']
)

install_requires = deps['chainalytic_viz']
extra_requires = deps
test_requires = deps['test']

with open('README.adoc') as readme_file:
    long_description = readme_file.read()

setup(
    name='chainalytic_viz',
    version='0.0.1',
    description='Data visualization for chainalytic-framework',
    long_description=long_description,
    long_description_content_type='text/asciidoc',
    author='duyyudus',
    author_email='duyyudus@gmail.com',
    url='https://github.com/duyyudus/chainalytic-visualizer',
    include_package_data=True,

    tests_require=test_requires,
    install_requires=install_requires,
    extras_require=extra_requires,

    license='MIT',
    zip_safe=False,
    keywords='blockchain data visualization',
    python_requires='>=3.7',

    packages=find_packages(
        where='src',
        exclude=['tests', 'tests.*', '__pycache__', '*.pyc']
    ),
    package_dir={
        '': 'src',
    },
    package_data={
        '': ['**/*.yml']
    },

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.7',
    ],
)
