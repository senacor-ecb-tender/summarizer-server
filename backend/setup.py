import setuptools

setuptools.setup(
    name='ecb_summarizer',
    version='0.0.1',
    description='Web server for a simple UI and for handling the communication with inference server.',
    install_requires=[],
    package_dir={'': 'summarizer', 'tests': 'tests'},
    packages=setuptools.find_packages('summarizer', 'tests'),
    test_suite='tests'
)
