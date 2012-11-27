install:
	sudo python setup.py install

clean:
	sudo rm -rf build dist sblog.egg-info

upload:
	sudo python setup.py sdist bdist_egg upload
