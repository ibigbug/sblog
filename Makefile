all: install clean

install:
	python2 setup.py install

clean:
	rm -rf build dist sblog.egg-info

upload:
	python2 setup.py sdist bdist_egg upload
