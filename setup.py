from setuptools import setup, find_packages
import sys, os

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()
NEWS = open(os.path.join(here, 'NEWS.md')).read()


version = '0.2'

install_requires = [
    # List your project dependencies here.
    # For more details, see:
    # http://packages.python.org/distribute/setuptools.html#declaring-dependencies
    'lxml', 'scikit-learn', 'nltk', 'hickle'
    ]

setup(name='jursegtok',
    version=version,
    description="legal domain specified tokenization",
    long_description=README + '\n\n' + NEWS,
    classifiers=[
      # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    ],
    keywords='tokenization python legal',
    author='Florian Kuhn',
    author_email='fkuhn@posteo.de',
    url='www.zeichenkette.de',
    license='Apache v2',
    package_data={
        'jursegtok': ['data/*']
    },
    packages=find_packages(),
    package_dir={'': 'src'}, include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    entry_points={
        'console_scripts':
            ['jursegtok=jursegtok.cli:main']
    }
)

