from setuptools import setup, find_packages


setup(
    name='markdown-blockdiag',
    version='0.5.0',
    packages=find_packages(),
    url='https://github.com/gisce/markdown-blockdiag',
    license='MIT',
    install_requires=[
        'Markdown',
        'blockdiag',
        'seqdiag',
        'actdiag',
        'nwdiag',
    ],
    author='GISCE-TI, S.L.',
    author_email='devel@gisce.net',
    test_suite="tests",
    description='blockdiag extension for Python Markdown'
)
