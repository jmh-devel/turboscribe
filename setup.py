from setuptools import setup, find_packages

setup(
    name="turboscribe",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        "python-dotenv"
    ],
    entry_points={
        "console_scripts": [
            # example entry point if needed in the future
        ],
    },
    author="Your Name",
    description="A Python client for the TurboScribe transcription API.",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)