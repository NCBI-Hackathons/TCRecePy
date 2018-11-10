from distutils.core import setup

setup(
        name='tumorstoppy',
        description='T-Cell classification of CDR3 subregions',
        long_description=open('README.md').read(),
        url='https://github.com/NCBI-Hackathons/TumorSTOp.py',
        version='0.1-dev',
        packages=['tumorstoppy',],
        install_requires=['numpy', 'scipy']
        )
