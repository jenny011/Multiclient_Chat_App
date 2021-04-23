from setuptools import setup, find_packages

setup(
    name='chat_room',
    version='1.0',
    long_description=__doc__,
    packages=find_packages(),
    include_package_data=False,
    zip_safe=False,
    install_requires=['Flask', 'Flask-SocketIO', 'flask-login', 'flask-cors', 'Werkzeug']
)
