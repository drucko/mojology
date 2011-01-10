mojology
========

Mojology is a simple application to browse syslog messages stored in a
`MongoDB`_ store, as logged by `syslog-ng`_, using the `mongodb
destination driver`_.

For the curious, there is a `demo`_ available with a small set of log
data.

Features
--------

 * Easy installation & configuration
 * A neat & lean web interface to browse logs
 * Built upon solid foundations:
   * `Flask`_
   * `PyMongo`_
   * HTML5 & AJAX - and degrades gracefully (usable even with lynx!)

Installation
------------

The easiest way to install the application is to make use of
virtualenv and pip - though, if one's distribution of choice has the
appropriate packages available, and globally installed, that works
just aswell. One will also need a recent version of the `mongodb
destination driver`_.

::

 $ git clone git://github.com/algernon/mojology.git
 $ virtualenv --no-site-packages mojology
 $ cd mojology
 $ . bin/activate
 $ pip install -r requirements.txt
 $ python server.py

This will start up the server with the default settings, and expects
that the database and collection are ready to be browsed.

On how to set up `syslog-ng`_ to create appropriate entries within our
collection, see the next section!

Configuration
-------------

Due to a design choice, mojology makes a few assumptions about the
documents in the browsed collection:

 * A few keys must be present, namely:
   * **ts**, containing the *$UNIXTIME* macro.
   * **host**, the host where the log is coming from (most often, this
     will be *$HOST*).
   * **log.facility** and **log.level**, the log's facility, and
     level, repsectively.
   * **program.name** and **program.pid**, as their name implies.
   * **message**, the message part of the log message.

Whatever else the document contains on the top level will be ignored
by mojology, except for a configurable key, which hosts a
sub-document, containing various, dynamic keys: such as the variables
produced with patterndb (or any other parser).

By default, this key is **dyn**.

To ease configuration, the following destination block will do just what mojology needs:

::

  destination d_mongo {
  	mongodb(
  		dynamic_values("dyn")
      		keys("ts", "host", "log.facility", "log.level", "program.name", "program.pid", "message")
  		values("$UNIXTIME", "$HOST", "$FACILITY", "$LEVEL", "$PROGRAM", "$PID", "$MSGONLY")
  	);
  };
  
Sprinkle the log block with some patterndb or other parser magic, and you're good to go!

If one wants to configure mojology itself, the best course of action
is to copy the **mojology/default_settings.py** file to the root
directory, along with **server.py**, and change values therein.

Alternatively, setting the **MOJOLOGY_SETTINGS** environment variable
to the path of the desired configuration file will work just as well.

License
-------

mojology is built upon free software, and is itself free aswell,
released under the `GNU GPL`_ (version 3 or later).

The source code is available from `github`_.

.. _MongoDB: http://www.mongodb.org/
.. _syslog-ng: http://www.balabit.com/network-security/syslog-ng/opensource-logging-system
.. _mongodb destination driver: http://asylum.madhouse-project.org/projects/syslog-ng/mongodb/
.. _Flask: http://flask.pocoo.org/
.. _PyMongo: https://github.com/mongodb/mongo-python-driver/
.. _GNU GPL: http://www.gnu.org/licenses/gpl.html
.. _github: https://github.com/algernon/mojology
.. _demo: http://mojology.madhouse-project.org/
