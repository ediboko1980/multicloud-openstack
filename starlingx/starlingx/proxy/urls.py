# Copyright (c) 2019 Intel Corporation.
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

from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from starlingx.proxy.views import identityV3
from starlingx.proxy.views import services
from newton_base.proxy import dnsaasdelegate

URLPATTERNS = [
    #    url(r'^identity/v2)$',
    #        identityV2.Tokens.as_view()),
    url(r'^identity/v3/auth/tokens/?$',
        identityV3.Tokens.as_view()),
    url(r'^identity/v3/?$',
        identityV3.Tokens.as_view()),
    url(r'^identity/v2.0/?$',
        identityV3.TokensV2.as_view()),
    url(r'^identity/v2.0/tokens/?$',
        identityV3.TokensV2.as_view()),
    url(r'^identity/v2.0/tenants/?$',
        services.GetTenants.as_view()),
    url(r'dns-delegate/(?P<requri>[0-9a-zA-Z./_-]*)$',
        dnsaasdelegate.DnsaasDelegate.as_view()),
    url(r'^(?P<servicetype>[0-9a-zA-Z]{,18})/(?P<requri>[0-9a-zA-Z./_-]*)$',
        services.Services.as_view()),
]

urlpatterns = format_suffix_patterns(URLPATTERNS)
