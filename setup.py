# Classification (U)

"""Program:  setup.py

    Description:  A setuptools based setup module.

"""

# Libraries and Global Variables

# Standard
import os
import setuptools

# Third-party

# Local
import version


# Read in long description from README file.
here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "README.md")) as f_hdlr:
    LONG_DESCRIPTION = f_hdlr.read()

setuptools.setup(
    name="Pulled_Search",
    description="Search for entries for Pulled Products.",
    author="Mark Pernot",
    author_email="Mark.J.Pernot@coe.ic.gov",
    url="https://sc.appdev.proj.coe.ic.gov/JAC-DSXD/pulled-search",
    version=version.__version__,
    platforms=["Linux"],
    long_description=LONG_DESCRIPTION,

    classifiers=[
        # Common Values:
        #  1 - Pre-Alpha
        #  2 - Alpha
        #  3 - Beta
        #  4 - Field
        #  5 - Production/Stable
        "Development Status :: 2 - Alpha",
        "Operating System :: Linux",
        "Operating System :: Linux :: Centos",
        "Operating System :: Linux :: Ubuntu",
        "Topic :: Database :: RabbitMQ",
        "Topic :: Database :: RabbitMQ :: 3.6.6",
        "Topic :: Database :: Mongodb",
        "Topic :: Database :: Mongodb :: 3.4.2",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6.6",
        "Programming Language :: Python :: 2.7.5"])
