DEBUG_DEST_DIR = /tmp/sblog_test_env/dst/static
DEST_DIR = ../static
SOURCE = sblog.styl
TARGET = sblog.css

all: sblog.css copy

debug: sblog.css copy-debug

sblog.css: $(SOURCE)
	stylus -c $(SOURCE)

copy-debug:
	cp $(TARGET) $(DEBUG_DEST_DIR)

copy: $(TARGET)
	cp $(TARGET) $(DEST_DIR)

.PHONY: clean
clean:
	rm $(TARGET)
