from setuptools import setup, find_packages

setup(
    name='h3_utils',
    version='0.1.0',
    description='H3 Utils',
    author='Shoaib & Hassan',
    packages=find_packages(),
    install_requires=[
        'h3==3.7.6',
        'folium',
        'shapely==2.0.1'
    ],
    entry_points={
        # 'console_scripts': [
        #     'h3_utils = h3_utils.__main__:main',
        # ],
    },
    author_email='saburq@gmail.com,hmushtaq720@gmail.com',
    url='https://github.com/sabman/h3_utils',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ],
    keywords='h3, folium, hexagon, hexagonal, hexagonal grid, hexagonal grid system',
    python_requires='>=3.6',
)
