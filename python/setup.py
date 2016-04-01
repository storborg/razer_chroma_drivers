from __future__ import print_function

from setuptools import setup, find_packages


setup(name='razerdriver',
      version='0.0.1.dev',
      description='Python interface to Razer Chroma Driver',
      long_description='',
      classifiers=[],
      keywords='razer chroma kernel driver led keyboard',
      url='https://github.com/storborg/razer_chroma_driver',
      author='Scott Torborg',
      author_email='storborg@gmail.com',
      license='GPL',
      packages=find_packages(),
      install_requires=[
      ],
      test_suite='nose.collector',
      tests_require=['nose'],
      include_package_data=True,
      zip_safe=False)
