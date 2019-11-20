# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from .Settings import Settings
from google.cloud import datastore

def from_datastore(entity):
    """Translates Datastore results into the format expected by the
    application.

    Datastore typically returns:
        [Entity{key: (kind, id), prop: val, ...}]

    This returns:
        [ name, street, city, state, zip, open_hr, close_hr, phone, drink, rating, website ]
    where name, street, city, state, open_hr, close_hr, phone, drink, and website are Python strings
    and where zip and rating are Python integers
    """
    if not entity:
        return None
    if isinstance(entity, list):
        entity = entity.pop()
    return [entity['api_key']]

class settings(Settings):
    def __init__(self):
        self.client = datastore.Client('bobaguide')

    def select(self, name):
        query = self.client.query(kind = 'Settings')
        entities = list(map(from_datastore,query.fetch()))
        return entities
