mojology
========

Mojology is a simple application to browse syslog messages stored in a
`MongoDB`_ store, as logged by `syslog-ng`_, using the `mongodb
destination driver`_.

A little bit of extra configuration is necessary for the driver to
produce a document structure that is expected by mojology: dynamic
values need to be under the **dyn** key, the **date** key must be a
*$UNIXTIME* macro, the *log level* and *facility* variables need to be
in the **log.level** and **log.facility** keys, with the *program
name* and the *pid* similarly under **program.name** and
**program.pid**.

The document also needs to contain a **message** key.

Any other key than these is ignored, unless it is below dyn.

To ease configuration, the following destination block will do just what mojology needs:

::

  destination d_mongo {
  	mongodb(
  		dynamic_values("dyn")
      		keys("date", "host", "log.facility", "log.level", "program.name", "program.pid", "message")
  		values("$UNIXTIME", "$HOST", "$FACILITY", "$LEVEL", "$PROGRAM", "$PID", "$MSGONLY")
  	);
  };
  
Sprinkle the log block with some patterndb or other parser magic, and you're good to go!

mojology itself is built using `Flask`_ and `PyMongo`_, and is
licensed under the `GNU GPL`_  (version 3 or later).

The source code is available from `github`_.

.. _MongoDB: http://www.mongodb.org/
.. _syslog-ng: http://www.balabit.com/network-security/syslog-ng/opensource-logging-system
.. _mongodb destination driver: http://asylum.madhouse-project.org/projects/syslog-ng/mongodb/
.. _Flask: http://flask.pocoo.org/
.. _PyMongo: https://github.com/mongodb/mongo-python-driver/
.. _GNU GPL: http://www.gnu.org/licenses/gpl.html
.. _github: https://github.com/algernon/mojology
