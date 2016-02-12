from setuptools import setup, find_packages

setup(
    name="systemhccake",
    version="0.0.1",
    author="Witold Wolski",
    maintainer=['Witold Wolski'],
    author_email="wewolski@gmail.com",
    maintainer_email=['wewolski@gmail.com'],
    description="",
    license="BSD",
    packages=find_packages(),
    url='https://github.com/systemhc/systemhc',
    install_requires=['Unimod','applicake', 'pyteomics', 'ruffus', 'configobj', 'searcake']
)
