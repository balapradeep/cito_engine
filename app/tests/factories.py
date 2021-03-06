"""Copyright 2014 Cyrus Dasadia

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import factory
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
import cito_engine.models
import rules_engine.models


class PluginServerFactory(factory.DjangoModelFactory):
    class Meta:
        model = cito_engine.models.PluginServer
    name = 'Factory Plugin Server'
    url = 'http://factory_plugin_server'


class PluginFactory(factory.DjangoModelFactory):
    class Meta:
        model = cito_engine.models.Plugin
    server = factory.LazyAttribute(lambda n: PluginServerFactory())
    name = 'Factory Plugin'


class TeamFactory(factory.DjangoModelFactory):
    class Meta:
        model = cito_engine.models.Team
    name = 'The_A_Team'
    description = factory.Sequence(lambda n: 'Team #{0}'.format(n))


class CategoryFactory(factory.DjangoModelFactory):
    class Meta:
        model = cito_engine.models.Category
    categoryType = 'CPU'


class EventFactory(factory.DjangoModelFactory):
    class Meta:
        model = cito_engine.models.Event
    summary = factory.Sequence(lambda n: 'Event #{0}'.format(n))
    description = 'A factory made event!'
    team = factory.LazyAttribute(lambda n: TeamFactory())
    category = factory.LazyAttribute(lambda n: CategoryFactory())


class IncidentFactory(factory.DjangoModelFactory):
    class Meta:
        model = cito_engine.models.Incident
    event = factory.LazyAttribute(lambda n: EventFactory())
    lastEventTime = timezone.now()
    element = factory.Sequence(lambda n: 'host{0}.citoenginetests.com'.format(n))


class IncidentLogFactory(factory.DjangoModelFactory):
    class Meta:
        model = cito_engine.models.IncidentLog
    incident = factory.LazyAttribute(lambda n: IncidentFactory())
    msg = factory.Sequence(lambda n: 'msg{0}'.format(n))


class EventActionFactory(factory.DjangoModelFactory):
    class Meta:
        model = cito_engine.models.EventAction
    event = factory.LazyAttribute(lambda n: EventFactory())
    plugin = factory.LazyAttribute(lambda n: PluginFactory())
    pluginParameters = '[ "__EVENTID__","__MESSAGE__","__INCIDENTID__"]'
    threshold_count = 1
    threshold_timer = 60


class EventActionCounterFactory(factory.DjangoModelFactory):
    class Meta:
        model = cito_engine.models.EventActionCounter
    incident = factory.LazyAttribute(lambda n: IncidentFactory())
    event_action = factory.LazyAttribute(lambda n: EventActionFactory())


class EventActionLogFactory(factory.DjangoModelFactory):
    class Meta:
        model = cito_engine.models.EventActionLog
    incident = factory.LazyAttribute(lambda n: IncidentFactory())
    event_action = factory.LazyAttribute(lambda n: EventActionFactory())
    text = factory.Sequence(lambda n: 'factory made event_action_log {0}'.format(n))


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User
    first_name = factory.Sequence(lambda n: "First%s" % n)
    last_name = factory.Sequence(lambda n: "Last%s" % n)
    email = factory.Sequence(lambda n: "email%s@example.com" % n)
    username = factory.Sequence(lambda n: "email%s@example.com" % n)
    password = make_password("password")
    is_staff = False


class EventSuppressorFactory(factory.DjangoModelFactory):
    class Meta:
        model = rules_engine.models.EventSuppressor
    event = factory.LazyAttribute(lambda n: EventFactory())
    suppressed_by = factory.LazyAttribute(lambda n: UserFactory())


class ElementSuppressorFactory(factory.DjangoModelFactory):
    class Meta:
        model = rules_engine.models.ElementSuppressor
    element = factory.Sequence(lambda n: 'host{0}.citoenginetests.com'.format(n))
    suppressed_by = factory.LazyAttribute(lambda n: UserFactory())


class EventAndElementSuppressorFactory(factory.DjangoModelFactory):
    class Meta:
        model = rules_engine.models.EventAndElementSuppressor
    event = factory.LazyAttribute(lambda n: EventFactory())
    element = factory.Sequence(lambda n: 'host{0}.citoenginetests.com'.format(n))
    suppressed_by = factory.LazyAttribute(lambda n: UserFactory())
