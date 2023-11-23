#CPPFLAG=-I/opt/homebrew/include

all: client

client : client.c
# For a Mac with a localized install via homebrew
#	gcc -I/opt/homebrew/include -L/opt/homebrew/lib c-zmq.c -l zmq -o czmq
# Otherwise use
	gcc client.c -l zmq -o client

clean:
	rm client
