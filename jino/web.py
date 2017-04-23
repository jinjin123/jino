# Copyright 2017 Arie Bregman
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
from configparser import ConfigParser
from flask import Flask
from gevent.pywsgi import WSGIServer
import logging
import os

from jino.views import webapp
logger = logging.getLogger(__name__)


class Web(object):
    """Jino Web Application."""

    DEFAULT_BIND_HOST = '0.0.0.0'
    DEFAULT_PORT = 5000
    DEFAULT_CONFIG_FILE = '/etc/jino/jino.conf'

    def __init__(self, args_ns):

        # Loads configuartion based on passed user arguments
        self.config = self._load_config_from_cli(args_ns)
        config_f = vars(args_ns)['config_file'] or self.DEFAULT_CONFIG_FILE
        if os.path.exists(config_f):
            self._load_config_from_file(config_f)

        # Creates flask application and registers the blueprints
        self.app = self.create_app(self.config)
        self.app.register_blueprint(webapp)

        self._setup_logging()

    def create_app(self, config):
        """Returns Flask application."""
        app = Flask(__name__)
        app.config.update(config)

        return app

    def _load_config_from_cli(self, args_ns):
        """Load arguments as passed by the user.

        returns dictionary of configartion options and their values.
        """
        config = {}

        # Convert Namespace instance into a dictionary of args:values
        # so we can load them into Flask configuration
        for k, v in vars(args_ns).iteritems():
            config[k.upper()] = v

        return config

    def _load_config_from_file(self, config_f):
        """Loads configuration from file."""
        config_file = ConfigParser.ConfigParser()
        config_file.read(config_f)

        for section in config_file.sections():
            for option in config_file.options(section):
                    self.config[option] = config_file.get(section, option)

    def _setup_logging(self):
        """Setup logging level."""
        format = '%(levelname)s: %(name)s | %(message)s'
        level = logging.DEBUG if self.app.config.get(
            'JINO_DEBUG') else logging.INFO
        logging.basicConfig(level=level, format=format)
        logging.getLogger(__name__)

    def run(self):
        """Runs the web server."""
        logger.info("Running Jino web server")

        log = 'default' if self.app.debug else None
        listen_socket = (
            self.app.config.get('BIND_HOST', self.DEFAULT_BIND_HOST),
            self.app.config.get('PORT', self.DEFAULT_PORT)
        )

        self.server = WSGIServer(listen_socket,
                                 application=self.app,
                                 log=log)
        self.server.serve_forever()