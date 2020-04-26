import setuptools

setuptools.setup(
    name='postkit',
    version='0.1.0',
    author='Ivan Cheltsov',
    author_email='chip.pragma@gmail.com',
    packages=setuptools.find_packages('.'),
    install_requires=[
        'furl',
        'requests',
        'pyyaml'
    ],
    python_requires='>=3.7'
)