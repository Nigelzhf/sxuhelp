from distutils.core import setup,Extension
moduleone=Extension('cetdes',
        sources=['pycet.c'],
        include_dirs=['/usr/local/opt/openssl/include'],
        library_dirs=['/usr/local/opt/openssl/lib'],
        libraries = ['crypto']
        )
setup(name='cetdes',
    version='1.0',
    description='This is cetdes',
    ext_modules=[moduleone]
)
