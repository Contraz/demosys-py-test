from setuptools import setup, find_packages
from pip.req import parse_requirements


def reqs_from_requirements_file():
    reqs = parse_requirements('requirements.txt', session='hack')
    return [str(r.req) for r in reqs]


setup(
    name="testdemo",
    version="0.0.1",
    description="Test project for demosys-py",
    long_description=open('README.rst').read(),
    url="https://github.com/Contraz/demosys-py-test",
    author="Einar Forselv",
    author_email="eforselv@gmail.com",
    maintainer="Einar Forselv",
    maintainer_email="eforselv@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    keywords = ['opengl', 'framework'],
    classifiers=[
        'Programming Language :: Python',
        'Environment :: MacOS X',
        'Environment :: X11 Applications',
        'Intended Audience :: Developers',
        'Topic :: Multimedia :: Graphics',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
    install_requires=reqs_from_requirements_file(),
    entry_points={'console_scripts': [
        'testdemo = testdemo.main:main',
    ]},
)
