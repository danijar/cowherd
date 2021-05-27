import setuptools
import pathlib


setuptools.setup(
    name='cowherd',
    version='0.2.0',
    description='Partially-observed visual reinforcement learning domain.',
    url='http://github.com/danijar/cowherd',
    long_description=pathlib.Path('README.md').read_text(),
    long_description_content_type='text/markdown',
    packages=['cowherd'],
    package_data={'cowherd': ['data.yaml', 'assets/*']},
    entry_points={'console_scripts': ['cowherd=cowherd.run_gui:main']},
    install_requires=['numpy', 'imageio', 'pillow', 'ruamel.yaml'],
    extras_require={'gui': ['pygame']},
    classifiers=[
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Games/Entertainment',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
)
