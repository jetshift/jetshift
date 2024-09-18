from setuptools import setup, find_packages


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
            'jetshift=jetshift_core.commands.main:main',
        ],
    },
)
