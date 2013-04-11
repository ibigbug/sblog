install:
	sudo python2 setup.py install

clean:
	sudo rm -rf build dist sblog.egg-info

upload:
	sudo python2 setup.py sdist bdist_egg upload
