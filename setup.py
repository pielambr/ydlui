from distutils.core import setup
import py2exe

setup(
    name='YdlUI',
    version='0.1',
    packages=[''],
    url='http://www,pielambr.be',
    license='MIT',
    author='Pieterjan Lambrecht',
    author_email='me@pielambr.be',
    description='GUI for youtube-dl',
    console=['main.py']
)
