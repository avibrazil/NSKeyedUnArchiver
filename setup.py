import setuptools
from NSKeyedUnArchiver import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="NSKeyedUnArchiver",
    version=__version__,
    author="Avi Alkalay",
    author_email="avibrazil@gmail.com",
    description="Decodes Apple's NSKeyedArchiver that were archived into text or binary plist files and returns a usable Python dict",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/avibrazil/NSKeyedUnArchiver",
#     install_requires=['biplist','pycryptodome'],
    packages=setuptools.find_packages(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Markup",
    ],
    python_requires='>=3.8',
)
