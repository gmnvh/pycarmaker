#include <stdio.h>
#include <winsock2.h>
#include <windows.h>
#include <time.h>

/* Include this if compiling suing Visual Studio */
#include <ws2tcpip.h>
#pragma comment(lib,"ws2_32.lib") //Winsock Library

#include "apo.h"

/* Step 1
 * Open CarMaker, load a TestRun and start the simulation
 */

/* Step 2
 * Execute this application and remember to restart it everytime you change the TestRun.
 * This code is an example and it is very simple. It does not handle changes in the Data Dictionary.
 */

int main()
{
    const int channel = 2;

    printf("APO Example - Reading vehicle speed");

    /* Initialize APO library */
    int rsp = ApocInit();
    printf("APO Init: %d\r\n", rsp);

    /* Servers query */
    rsp = ApocQueryServers(2 * 1000, "localhost");
    printf("APO QueryServers: %d\r\n", rsp);

    while (!ApocQueryDone())
    {
        ApocPoll();
        Sleep(100);
    }

    printf("APO Query Servers Done: %d servers found\r\n", ApocGetServerCount());

    /* Show found servers */
    for (int i = 0; i < ApocGetServerCount(); i++)
    {
        const tApoServerInfo* sinf = ApocGetServer(i);
        printf("Server: %s\r\n", sinf->Identity);
    }

    tApoSid sid = NULL;

    /* If you have CarMaker only as a server this will be always 0 */
    sid = ApocOpenServer(0);

    if (sid == NULL)
    {
        printf("Open Server Error");
        return 0;
    }

    /* Connect to server */
    rsp = ApocConnect(sid, 1 << channel);
    printf("Connect: %d\r\n", rsp);
    
    while (ApocGetStatus(sid, NULL) == ApoConnPending)
    {
        ApocPoll();
        ApoSleep_ms(100);
        printf("Waiting to connect\r\n");
    }

    rsp = ApocGetStatus(sid, NULL);
    printf("Server status after connect: %s\r\n", ApoStrStatus(rsp));

    if (!(ApocGetStatus(sid, NULL) & ApoConnUp))
    {
        printf("Connection failed");
        return 0;
    }

    rsp = ApocGetQuantCount(sid);
    printf("Number of quantities: %d\r\n", rsp);

    /* Show all quantities that starts with Car.v */
    for (int i = 0; i < rsp; i++)
    {
        const tApoQuantInfo* qinf = ApocGetQuantInfo(sid, i);
        if (strncmp(qinf->Name, "Car.v", 5) == 0)
        {
            printf("%s [%s]\n", qinf->Name, qinf->Unit);
        }
    }

    /* Subscribe to Time and Car.v */
    tApoSubscription subs[2];
    subs[0].Name = "Car.v";
    subs[1].Name = "Time";

    rsp = ApocSubscribe(sid, 2, subs, 50, 1, 10, 0);
    printf("Subscribe of quantities: %d\r\n", rsp);

    rsp = ApocGetStatus(sid, NULL);
    printf("Server status after subscribe: %s\r\n", ApoStrStatus(rsp));

    int seq;
    int msglen, msgch;
    char msgbuf[APO_ADMMAX];

    while (1)
    {
        if (ApocWaitIO(50) == 1) {
            ApocPoll();

            rsp = ApocGetStatus(sid, NULL);
            printf("Server status: %s - ", ApoStrStatus(rsp));

            if (!(ApocGetStatus(sid, NULL) & ApoConnUp))
            {
                ApoSleep_ms(50);
                break;
            }

            seq = ApocGetData(sid);
            printf("Seq: %03d - ", seq);

            while (seq > 0)
            {
                seq = ApocGetData(sid);
            }
            printf("Value of %s: Time: %6.3f: %3.3f", subs[0].Name, *((double*)subs[1].Ptr), *((float*)subs[0].Ptr));

            printf("\n\r");

            /* You must call this function even if not used. Please check APO.pdf section 2.1.2 Polling. */
            ApocGetAppMsg(sid, &msgch, msgbuf, &msglen);
            ApoSleep_ms(50);
        }
    }

    ApocCloseServer(sid);
    return 0;
}