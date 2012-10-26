#!/bin/bash
i18ndude rebuild-pot --pot src/collective/roster/locales/collective.roster.pot --create collective.roster src/collective/roster

i18ndude sync --pot src/collective/roster/locales/collective.roster.pot src/collective/roster/locales/*/LC_MESSAGES/collective.roster.po
