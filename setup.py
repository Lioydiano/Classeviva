#!\usr\bin\env python3


import setuptools
VERSION = "1.2.2"
setuptools.setup(
    name='Classeviva.py',
    packages=[
        'classeviva',
        'classeviva.eccezioni',
        'classeviva.collegamenti',
        'classeviva.variabili'
    ],
    package_dir={
        'classeviva': 'src/classeviva',
        'classeviva.eccezioni': 'src/classeviva/eccezioni',
        'classeviva.collegamenti': 'src/classeviva/collegamenti',
        'classeviva.variabili': 'src/classeviva/variabili',
    },
    version=VERSION,
    license='MIT',
    requires=["requests"],
    install_requires='requests>=2.27',
    description='Classeviva Python API wrapper',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='FLAK-ZOSO',
    author_email='mattia.marchese.2006@gmail.com',
    url='https://github.com/Lioydiano/Classeviva',
    download_url=f'https://github.com/Lioydiano/Classeviva/archive/refs/tags/v{VERSION}.tar.gz',
    keywords=[
        'classeviva', 
        'api'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: Implementation :: CPython",
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Natural Language :: Italian",
        "Natural Language :: English",
        "Typing :: Typed"
    ],
    python_requires=">=3.10"
)