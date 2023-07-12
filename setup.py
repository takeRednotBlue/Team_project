from setuptools import setup, find_namespace_packages, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    requirements = [
        line.split('#', 1)[0].strip() for line in f.read().splitlines()
        if not line.strip().startswith('#')
    ]


setup(
    name="bithive-bot",
    version='0.0.1',
    author="BitHive Team",
    description="Bot assistant for those who are in love with terminal.",
    long_description=long_description,
    url="https://github.com/takeRednotBlue/Team_project",
    license="MIT License",
    packages=find_namespace_packages(),
    include_package_data=True,
    install_requires=requirements,
    entry_points = {
        'console_scripts': [
            'start-bot = bithive_bot.src:menu_app'
        ]
    }
)
