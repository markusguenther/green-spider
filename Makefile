

.PHONY: webapp dockerimage

# Build docker image
dockerimage:
	docker pull debian:stretch-slim
	docker build -t spider .

# Run spider in docker image
spider: dockerimage
	docker run --rm -ti \
		-v $(PWD)/webapp/dist/data:/out \
		-v $(PWD)/docs/siteicons:/icons \
		spider

test: dockerimage
	docker run --rm -ti spider /spider_test.py

screenshots: venv
	venv/bin/python ./screenshots.py secrets/screenshot-reader.json

webapp/node_modules:
	cd webapp && npm install

# Build webapp
webapp: webapp/node_modules screenshots
	cd webapp && npx webpack --config webpack.config.js
	cp -r webapp/dist/* ./docs/
	cp webapp/node_modules/tooltipster/dist/css/tooltipster.bundle.min.css ./docs/css/
	rm webapp/dist/bundle.js

serve-webapp:
	cd docs && ../venv/bin/python -m http.server
