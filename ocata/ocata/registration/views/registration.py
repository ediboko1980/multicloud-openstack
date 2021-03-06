# Copyright (c) 2017-2018 Wind River Systems, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging

from django.conf import settings
from newton_base.registration import registration as newton_registration
from common.msapi import extsys

logger = logging.getLogger(__name__)

# DEBUG=True


class Registry(newton_registration.Registry):

    def __init__(self):
        self.proxy_prefix = settings.MULTICLOUD_PREFIX
        self.aai_base_url = settings.AAI_BASE_URL
        self._logger = logger
        super(Registry, self).__init__()


class RegistryV1(Registry):
    def __init__(self):
        self.proxy_prefix = settings.MULTICLOUD_API_V1_PREFIX
        self.aai_base_url = settings.AAI_BASE_URL
        self._logger = logger
        super(RegistryV1, self).__init__()

    def post(self, request, cloud_owner="", cloud_region_id=""):
        self._logger.info("registration with : %s, %s" % (cloud_owner, cloud_region_id))
        self._logger.debug("with data: %s" % request.data)

        vimid = extsys.encode_vim_id(cloud_owner, cloud_region_id)
        return super(RegistryV1, self).post(request, vimid)

    def delete(self, request, cloud_owner="", cloud_region_id=""):
        self._logger.debug("unregister cloud region: %s, %s" % (cloud_owner, cloud_region_id))

        vimid = extsys.encode_vim_id(cloud_owner, cloud_region_id)
        return super(RegistryV1, self).delete(request, vimid)
