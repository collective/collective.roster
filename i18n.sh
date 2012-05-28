#!/bin/bash
i18ndude rebuild-pot --pot src/jyu/roster/locales/jyu.roster.pot --create jyu.roster src/jyu/roster

i18ndude sync --pot src/jyu/roster/locales/jyu.roster.pot src/jyu/roster/locales/*/LC_MESSAGES/jyu.roster.po
