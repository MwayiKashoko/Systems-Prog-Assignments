CC=		gcc
CFLAGS=		-Wall -std=gnu99 -g
AR=		ar
ARFLAGS=	rcs
LD=		gcc
LDFLAGS=	-Llib
SRC := packet.c pcap-read.c pcap-process.c main.c
OBJ := $(SRC:.c=.o)

all: redextract

redextract: $(OBJ)
	$(CC) $(CFLAGS) $(OBJ) -o $@

%.o: %.c
	$(CC) $(CFLAGS) -c -o $@ $^

clean: 
	rm redextract
	rm *.o

