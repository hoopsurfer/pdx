pdx: pdx-base.deb

pdx-base.deb:
	dpkg -b pdx-base/ pdx-base.deb

clean: pdx-base.deb
	rm -f pdx-base.deb

install: pdx-base.deb
	sudo dpkg -i pdx-base.deb

test:
	cp pdx-base/usr/share/pdx/script/pdx-check       /usr/share/pdx/script
	cp pdx-base/usr/share/pdx/script/pdx-clonessd    /usr/share/pdx/script
	cp pdx-base/usr/share/pdx/python/pdx-bootssd.py  /usr/share/pdx/python
	cp pdx-base/usr/share/pdx/python/pdx-fixrtc.py   /usr/share/pdx/python
	cp pdx-base/usr/share/pdx/python/pdx-powerkey.py /usr/share/pdx/python
	cp pdx-base/usr/share/pdx/python/pdx-poweroff.py /usr/share/pdx/python

uninstall:
	sudo dpkg -r pdx-base
