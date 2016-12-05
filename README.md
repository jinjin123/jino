Jino
====

Jino is a dashboard, used for managing and monitoring Jenkins.

Installation
------------

To install jino, run the following command:

    sudo pip install jino

Usage
-----

Jino requires several arguments in order to run properly:

* Jenkins URL   - the url of your Jenkins server (e.g http://my_jenkins)
* Username      - Jenkins username
* Password      - Jenkins password
* Jobs YAML - Jino will build the home page tables based on this file

To run Jino::

    jino runserver --jenkins 'http://my_jenkins' --username X --password Y --jobs /etc/jobs.yaml

OR

    jino runserver --conf /etc/jino.cfg --jobs /etc/jobs.yaml

CONFIGURATION
-------------

You must specify three variables::

     JENKINS = http://<your_jenkins_server>
     USERNAME = <Jenkins user>
     PASSWORD = <Jenkins user password>

The location specified by --conf. By default, Jino will look for /etc/jino/config.cfg.

JOBS
----

Using YAML format::

    - table: neutron
      jobs:
		- title: "Title of the first row"
		  name: "jenkins-job-name1"

		- title: "Title of the second row"
		  name: "jenkins-job-name2"

The location specified by --jobs. By default, Jino will look for /etc/jino/jobs.yaml.
