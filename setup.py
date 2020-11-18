from setuptools import setup, find_packages
from kicad_tools import __version__

setup(
    name='js_serial',
    version=__version__,
    description='Bridge between javascript app and serial device',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/danidask/js_serial',
    author='Daniel Alvarez',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'eventlet',
        'python-socketio',
        'pyserial'
    ],
    python_requires='>=3.5',
    entry_points={
        "console_scripts": [
            "js_serial = js_serial.js_serial_server:main",
        ]
    }
)
