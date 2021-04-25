SHELL=/bin/bash
export SHELL
APP := $(shell pwd)

all: run_app $(APP)/run.sh $(APP)/setup.py $(APP)/run.py $(APP)/chat_room

.PHONY: run_app $(APP)/run.sh $(APP)/setup.py $(APP)/run.py $(APP)/chat_room

run_app: $(APP)/run.sh $(APP)/setup.py $(APP)/run.py $(APP)/chat_room
	@bash $(APP)/run.sh $(APP)
