from setuptools import setup, find_packages

def _requires_from_file(filename):
    return open(filename).read().splitlines()


setup(
    name='camera-mouse-controller',
    version='3.0.0',
    packages=find_packages(),
    description='A webcam-based virtual gesture mouse controller powered by MediaPipe hand tracking',
    author='CeatursHarmginton',
    author_email='',
    url='https://github.com/CeatursHarmginton/camera-mouse-controller',
    license='Apache-2.0',
    install_requires=_requires_from_file('requirements.txt'),
    entry_points={'console_scripts': ['nonmouse=nonmouse.__main__:main',]},
    python_requires='>=3.8',
)
