# -*- coding: utf-8 -*-
"""Family module for Wikimedia Commons."""
#
# (C) Pywikibot team, 2005-2015
#
# Distributed under the terms of the MIT license.
#
from __future__ import absolute_import, unicode_literals

__version__ = '$Id: f3670016b6c701351df140b7a9932d09bb44ce00 $'

from pywikibot import family


# The Wikimedia Commons family
class Family(family.WikimediaOrgFamily):

    """Family class for Wikimedia Commons."""

    name = 'commons'

    def __init__(self):
        """Constructor."""
        super(Family, self).__init__()

        self.interwiki_forward = 'wikipedia'

        self.category_redirect_templates = {
            'commons': (
                u'Category redirect',
                u'Categoryredirect',
                u'Catredirect',
                u'Cat redirect',
                u'Catredir',
                u'Cat-red',
                u'See cat',
                u'Seecat',
                u'See category',
                u'Redirect category',
                u'Redirect cat',
                u'Redir cat',
                u'Synonym taxon category redirect',
                u'Invalid taxon category redirect',
                u'Monotypic taxon category redirect',
            ),
        }

        # Subpages for documentation.
        self.doc_subpages = {
            '_default': ((u'/doc', ), ['commons']),
        }
