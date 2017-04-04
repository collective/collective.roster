#!/usr/bin/env bash
bin/i18ndude rebuild-pot --pot src/collective/roster/locales/collective.roster.pot --merge src/collective/roster/locales/manual.pot --create collective.roster src/collective/roster
bin/i18ndude sync --pot src/collective/roster/locales/collective.roster.pot src/collective/roster/locales/*/LC_MESSAGES/collective.roster.po
bin/pocompile
