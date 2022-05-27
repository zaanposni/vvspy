from setuptools import setup, find_packages

with open("readme.md", "r") as fh:
    long_description = fh.read()

setup(
  name='vvspy',
  py_modules=["vvspy"],
  version='1.1.4',
  license='MIT',
  description='API Wrapper for VVS (Verkehrsverbund Stuttgart)',
  author='zaanposni',
  author_email='zaanposni@users.noreply.github.com',
  url='https://github.com/FI18-Trainees/vvspy',
  keywords=['VVS', 'API', 'STUTTGART', 'WRAPPER', 'JSON', 'REST', 'EFA', 'PYTHON'],
  packages=find_packages(exclude=["*tests"]),
  package_data={
    "vvspy": ["vvspy/*"]
  },
  install_requires=[
          'requests',
          'typing',
      ],
  classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
  long_description=long_description,
  long_description_content_type="text/markdown"
)
