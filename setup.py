from setuptools import setup, find_packages

setup(
    name="pynbp",
    version='1.0.0',
    description="tidy downloading of National Bank of Poland interest rates, FX rates and gold price data",
    author_email="awegrzyn17@gmail.com",
    author="Artur Wegrzyn",
    packages=find_packages(exclude=["tests"]),
    install_requires=[
        'certifi>=2022.12.7',
        'charset-normalizer>=3.1.0',
        'idna>=3.4',
        'numpy>=1.24.3',
        'pandas>=2.0.1',
        'python-dateutil>=2.8.2',
        'pytz>=2023.3',
        'requests>=2.29.0',
        'six>=1.16.0',
        'tzdata>=2023.3',
        'urllib3>=1.26.15'
    ]
)
