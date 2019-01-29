import setuptools


with open("README.md", "r") as readme_file:
    long_description = readme_file.read()


setuptools.setup(
    name='iter2',
    version='1.0',
    description='Implementation of some rich-iterator concept',
    author='Shemyakin Roman',
    author_email='ramon93i7@gmail.com',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ramon93i7/iter2',
    license='MIT',
    packages=setuptools.find_packages('.', exclude=['tests', 'tests.*']),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License'
    ]
)
