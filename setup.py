"""
allows us to specify/type 'List'
"""
from typing import List
from setuptools import find_packages, setup

requirements = []


def get_requirements(filename: str) -> List[str]:
    """
    Gets the names of the requiered packages from 
    requirments.txt and returns them as a list
    reads file and returns --> ['numpy', 'pandas','matplotlib',...]
    """
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            if not line:  # if line is empty then skip
                continue
            requirements.append(line.strip().strip('\n'))
    if '-e .' in requirements:
        requirements.remove('-e .')
    print(requirements)
    return requirements


setup(
    name='Customer Churn Prediction',
    author='Jay Thanki',
    author_email='jayyoges@buffalo.edu',
    version='0.0.1',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt'))
