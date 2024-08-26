#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from httpx import Client


class OpencastClient(Client):

    def __init__(
            self,
            hostname,
            *args, **kwargs):
        super().__init__(base_url=hostname, *args, **kwargs)

