all: install clean

install:
	python setup.py install

clean:
	rm -rf build dist sblog.egg-info

upload:
	python setup.py register sdist bdist_egg upload
