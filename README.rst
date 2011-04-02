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
* Built upon solid foundations: `Flask`_, `PyMongo`_, and HTML5 &
  AJAX - and degrades gracefully (usable even with lynx!)

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

Though one can customize the database layout to some extent, how to do
that is out of the scope of this small document. Instead, we'll have a
look at how to set up syslog-ng to produce documents with which
mojology can work with.

By default, we only need a simple change: the **DATE** key must be a
*$UNIXTIME* macro. Apart from this, mojology does not make many more
assumptions, and by default, uses the same keys for the various bits
of information (host, program, message, etc) that syslog-ng uses by
default.

Thus, in order to get all the information mojology needs, along with
every discovered (by patterndb or similar) key, one could use the
following destination definition:

::

  destination d_mongo {
  	mongodb(
	        value-pairs(
			scope(selected_macros nv_pairs)
			exclude("R_*")
			exclude("S_*")
			exclude("HOST_FROM")
			exclude("LEGACY_MSGHDR")
			exclude("MSG")
			pair("DATE" "$UNIXTIME")
		)
	);
  };
  
Sprinkle the log block with some patterndb or other parser magic, and
you're good to go!

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
