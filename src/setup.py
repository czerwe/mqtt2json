from setuptools import setup, find_packages

setup(
    name="mqtt2json",
    version="0.1.0",
    description="Extract tracks from an mkv and add them to another mkv with an m4v Video",
    author="cze",
    author_email="ernest@czerwonka.de",
    packages=find_packages(),
    install_requires=[
        "Flask<=2",
        "prometheus-flask-exporter",
        "paho-mqtt",
        "gunicorn",
        "pyyaml",
        "python-dateutil",
        "pytz",
    ],
)
