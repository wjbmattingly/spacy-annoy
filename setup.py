from setuptools import setup, find_packages

setup(
    name='spacy-annoy',
    version='0.0.1',
    packages=find_packages(),
    url='https://github.com/wjbmattingly/spacy-annoy',
    license='MIT',
    author='WJB Mattingly',
    description='A Python package integrating Spacy and Annoy for efficient text search and analysis',
    install_requires=[
        'spacy>=3.0',
        'annoy>=1.17'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',  # Adjust based on your Python version
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Adjust based on your requirements
)
