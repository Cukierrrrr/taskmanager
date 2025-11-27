from setuptools import setup, find_packages
from taskmanager import VERSION

with open("requirements.txt") as file:
    requirements = file.readlines()

setup(
    name="task_manager",
    version=f"{VERSION[0]}.{VERSION[1]}.{VERSION[2]}",
    packages=find_packages(),
    install_requires=[r.strip() for r in requirements],
    description="Aplikacja do zarządzania zadaniami",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
    ],
    scripts=["manage.py"],
)
