=======
Hacking
=======


Running tests
=============

Install a virtualenv::

    virtualenv myenv

Activate virtualenv::

    source myenv/bin/activate

Install tox::

    pip install tox

To run all tests, you'll need python2.6, python2.7, and python3.2 installed.
With one or more of these Python versions installed, you should be able to run
some tests::

    cd python-archive
    tox
