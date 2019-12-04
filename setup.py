from setuptools import setup, find_packages


setup(
    name = 'Advanced-System-Design-Project',
    version = '0.1.0',
    author = 'May Gan',
    description = 'An example package.',
    packages = find_packages(),
    install_requires = ['click', 'flask'],
    tests_require = ['pytest', 'pytest-cov'],
)
