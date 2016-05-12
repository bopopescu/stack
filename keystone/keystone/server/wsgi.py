# Copyright 2013 OpenStack Foundation
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

import os

from oslo_config import cfg
import oslo_i18n
from oslo_log import log

from keystone.common import profiler


# NOTE(dstanek): i18n.enable_lazy() must be called before
# keystone.i18n._() is called to ensure it has the desired lazy lookup
# behavior. This includes cases, like keystone.exceptions, where
# keystone.i18n._() is called at import time.
oslo_i18n.enable_lazy()


from keystone.common import config
from keystone.server import common
from keystone.version import service as keystone_service


CONF = cfg.CONF


def initialize_application(name,
                           post_log_configured_function=lambda: None,
                           config_files=None):
    if not config_files:
        config_files = None

    common.configure(config_files=config_files)

    # Log the options used when starting if we're in debug mode...
    if CONF.debug:
        CONF.log_opt_values(log.getLogger(CONF.prog), log.DEBUG)

    post_log_configured_function()

    def loadapp():
        return keystone_service.loadapp(
            'config:%s' % config.find_paste_config(), name)

    _unused, application = common.setup_backends(
        startup_application_fn=loadapp)

    # setup OSprofiler notifier and enable the profiling if that is configured
    # in Keystone configuration file.
    profiler.setup(name)

    return application


def _get_config_files(env=None):
    if env is None:
        env = os.environ

    dirname = env.get('OS_KEYSTONE_CONFIG_DIR', '').strip()

    files = [s.strip() for s in
             env.get('OS_KEYSTONE_CONFIG_FILES', '').split(';') if s.strip()]

    if dirname:
        if not files:
            files = ['keystone.conf']
        files = [os.path.join(dirname, fname) for fname in files]

    return files


def initialize_admin_application():
    return initialize_application(name='admin',
                                  config_files=_get_config_files())


def initialize_public_application():
    return initialize_application(name='main',
                                  config_files=_get_config_files())
