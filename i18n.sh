#!/nix/store/28wl3f34vfjpw0y5809bgr6382wqdscf-bash-4.3-p48/bin/bash
bin/i18ndude rebuild-pot --pot src/collective/roster/locales/collective.roster.pot --merge src/collective/roster/locales/manual.pot --create collective.roster src/collective/roster
bin/i18ndude sync --pot src/collective/roster/locales/collective.roster.pot src/collective/roster/locales/*/LC_MESSAGES/collective.roster.po
bin/pocompile
