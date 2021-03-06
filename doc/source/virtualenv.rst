virtualenv
==========

If you want to merely test out the library, you can do that easily in a *virtual python environment*
created with `virtualenv`.


Setup
-----

The following steps set up an evironment:

* create a directory and initialize the environment

  .. code-block:: bash

     $ mkdir pwwtest
     $ virtualenv pwwtest

* install the required packages

  .. code-block:: bash

     $ pwwtest/bin/pip install numpy
     $ pwwtest/bin/pip install PIL
     $ pwwtest/bin/pip install matplotlib
     $ pwwtest/bin/pip install pygraphviz
     $ pwwtest/bin/pip install javabridge

* as an alternative, you can also use all currently installed packages on your
  host system in the virtual environment. For instance, on Ubuntu, run the following
  commands to install all the dependencies:

  .. code-block:: bash

     $ sudo apt-get install python-numpy python-imaging python-matplotlib python-pygraphviz
     $ sudo pip install javabridge

  after that, you can create the virtual environment as follows:

  .. code-block:: bash

     $ virtualenv --system-site-packages pwwtest

* a build environment is required to build libraries, like `javabridge`, from source. For Ubuntu that would
  be the `build-essential` meta-package and Xcode for Mac OSX.


Troubleshooting
---------------

* You may need to install the header files for the following libraries for the compilations to succeed:

  * freetype
  * graphviz
  * png

* Before you can install `matplotlib`, you may have to upgrade your `distribute` library as follows:

  .. code-block:: bash

     $  bin/easy_install -U distribute

* On Ubuntu, follow `this post <http://www.sandersnewmedia.com/why/2012/04/16/installing-pil-virtualenv-ubuntu-1204-precise-pangolin/>`_
  to install all the required dependencies for PIL:

  .. code-block:: bash

     $ sudo apt-get build-dep python-imaging

* To enable support for PIL on Ubuntu, see
  `this post <http://www.sandersnewmedia.com/why/2012/04/16/installing-pil-virtualenv-ubuntu-1204-precise-pangolin/>`_:

  .. code-block:: bash

     $ sudo ln -s /usr/lib/`uname -i`-linux-gnu/libfreetype.so /usr/lib/
     $ sudo ln -s /usr/lib/`uname -i`-linux-gnu/libjpeg.so /usr/lib/
     $ sudo ln -s /usr/lib/`uname -i`-linux-gnu/libz.so /usr/lib/

