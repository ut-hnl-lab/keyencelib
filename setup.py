from setuptools import setup

setup(
    name="KeyenceLib",
    version="0.1.0",
    license="MIT",
    description="Measurement package for Keyence laser profilers",
    author="KotaAono",
    url="https://github.com/ut-hnl-lab/keyencelib.git",
    packages=['keyencelib'],
    install_requires=[
        'matplotlib',
        'numpy'
    ]
)
