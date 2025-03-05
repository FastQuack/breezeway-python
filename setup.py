import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name='breezeway',
    version='0.1.0',
    author='Anthony Degarimore',
    author_email='Anthony@DeGarimore.com',
    description="Library for interacting with Breezeway's API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ]
)
