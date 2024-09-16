from setuptools import setup, find_packages


# Function to read requirements.txt
def parse_requirements(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file if line and not line.startswith("#")]


setup(
    name="jetshift",
    version="1.0.0-alpha.5",
    packages=find_packages(),
    include_package_data=True,
    install_requires=parse_requirements('requirements.txt'),
    entry_points={
        'console_scripts': [
            'dev=jetshift_core.runners.dev:main',
            'make=jetshift_core.stubs.make:main',
            'migrate=jetshift_core.runners.migration:main',
            'seed=jetshift_core.runners.seeder:main',
            'job=jetshift_core.runners.job:main',
            'quick=jetshift_core.runners.quicker:main',
        ],
    },
)
