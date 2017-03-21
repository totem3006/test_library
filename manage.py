#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import config

from migrate.versioning.shell import main


if __name__ == '__main__':
    main(url=config.SQLALCHEMY_DATABASE_URI, debug='False', repository='models')
