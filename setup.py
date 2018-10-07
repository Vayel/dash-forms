from setuptools import setup, find_packages

setup(
    name='dash-forms',
    url='https://github.com/Vayel/dash-forms',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'plotly',
        'dash',
        'dash-html-components',
        'dash-core-components',
    ],
)
