all: install clean

install:
	python setup.py install

clean:
	rm -rf build dist sblog.egg-info

upload:
	python2 setup.py sdist bdist_egg upload
