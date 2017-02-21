BUILDOUT_BIN ?= $(shell command -v buildout || echo 'bin/buildout')
FONTELLO_BIN ?= $(shell command -v fontello-svg || echo 'node_modules/.bin/fontello-svg')
BUILDOUT_ARGS ?=
PYBOT_ARGS ?=

STATIC = src/collective/roster/browser/static

all: build check

show: $(BUILDOUT_BIN)
	$(BUILDOUT_BIN) $(BUILDOUT_ARGS) annotate

build: $(BUILDOUT_BIN)
	$(BUILDOUT_BIN) $(BUILDOUT_ARGS)

docs: bin/pocompile bin/sphinx-build
	bin/pocompile
	LANGUAGE=fi bin/sphinx-build docs html

test: bin/pocompile bin/test bin/pybot bin/code-analysis
	bin/pocompile
	bin/test --all
	bin/code-analysis
	bin/pybot $(PYBOT_ARGS) -d parts/test docs

check: test

dist:
	@echo "Not implemented"

deploy:
	@echo "Not implemented"

watch: bin/instance
	RELOAD_PATH=src bin/instance fg

robot-server: bin/robot-server
	LANGUAGE=fi RELOAD_PATH=src bin/robot-server collective.roster.testing.ROSTER_ACCEPTANCE_TESTING -v

robot: bin/robot
	bin/robot -d parts/test docs

sphinx: bin/robot-sphinx-build
	bin/robot-sphinx-build -d html docs html

clean:
	rm -rf .installed bin develop-eggs parts

$(STATIC)/bundle.css: $(STATIC)/css/*.css
	cat $(STATIC)/css/*.css > $(STATIC)/bundle.css

$(STATIC)/icons: $(FONTELLO_BIN) fontello.json
	node_modules/.bin/fontello-svg --config fontello.json --no-css --verbose \
	  --out $(STATIC)/icons --fill-colors "black:rgb(0,0,0)|white:rgb(255,255,255)"

###

.PHONY: all show build docs test check dist deploy watch clean

node_modules: package.json
	npm install
	touch node_modules

node_modules/.bin/fontello-svg: node_modules

bootstrap-buildout.py:
	curl -k -O https://bootstrap.pypa.io/bootstrap-buildout.py

bin/buildout: bootstrap-buildout.py
	python bootstrap-buildout.py

bin/test: $(BUILDOUT_BIN)
	$(BUILDOUT_BIN) $(BUILDOUT_ARGS) install test

bin/pybot: $(BUILDOUT_BIN)
	$(BUILDOUT_BIN) $(BUILDOUT_ARGS) install pybot

bin/sphinx-build: $(BUILDOUT_BIN)
	$(BUILDOUT_BIN) $(BUILDOUT_ARGS) install sphinx-build

bin/robot: $(BUILDOUT_BIN)
	$(BUILDOUT_BIN) $(BUILDOUT_ARGS) install robot

bin/robot-server: $(BUILDOUT_BIN)
	$(BUILDOUT_BIN) $(BUILDOUT_ARGS) install robot

bin/robot-sphinx-build: $(BUILDOUT_BIN)
	$(BUILDOUT_BIN) $(BUILDOUT_ARGS) install robot

bin/instance: $(BUILDOUT_BIN)
	$(BUILDOUT_BIN) $(BUILDOUT_ARGS) install instance

bin/code-analysis: $(BUILDOUT_BIN)
	$(BUILDOUT_BIN) $(BUILDOUT_ARGS) install code-analysis

bin/isort: $(BUILDOUT_BIN)
	$(BUILDOUT_BIN) $(BUILDOUT_ARGS) install isort

bin/pocompile: $(BUILDOUT_BIN)
	$(BUILDOUT_BIN) $(BUILDOUT_ARGS) install i18ndude
