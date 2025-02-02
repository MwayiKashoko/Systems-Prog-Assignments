//  Go Irish client
#include <zmq.h>
#include <string.h>
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

#define ZMQ_SERVER_PORT 40872

int main (void)
{
    int rc;             /* Save the return code */

    printf ("Connecting to the beacon server...\n");
    void *context = zmq_ctx_new ();
    void *requester = zmq_socket (context, ZMQ_REQ);

    char pszRequest[25];
    sprintf(pszRequest, "tcp://localhost:%d", ZMQ_SERVER_PORT);

    rc = zmq_connect (requester, pszRequest);

    if(rc == 0)
    {
        /* If this printf is printed, the network is working */
        printf("  Successfully connected\n");
    }
    else 
    {
        printf("  Network connection failed\n");
        exit(-1);
    }

    int request_nbr;
    char buffer [BUFSIZ];

    for (request_nbr = 0; ; request_nbr++) {
        printf ("Sending beacon %d...\n", request_nbr);

        char input[BUFSIZ];
        fgets(input, BUFSIZ, stdin);

        if (strcmp("exit\n", input) == 0) {
          break;
        }

        zmq_send (requester, input, strlen(input), 0);

        memset(buffer, 0, BUFSIZ);
        zmq_recv (requester, buffer, BUFSIZ, 0);
        printf ("Received %s (Message %d)\n", buffer, request_nbr);
    }
    zmq_close (requester);
    zmq_ctx_destroy (context);
    return 0;
}


