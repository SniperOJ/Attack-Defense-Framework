1. modify watch.py, add auth method(user/pass or public key file)(search `TODO`)  
2. `bash sync.sh src dst true`  
    * src: folder absolute path in local file system  
    * dst: folder absolute path in ssh server  
    eg:   
        `bash sync.sh /root/flows /data/flows true`
    (make sure that folders exist)  
  
dir structure:  

```
.
├── 36a8635b-2127-4740-a75f-b47102e2172a # Task ID
│   ├── 2018-08-08.19:50:09.pcap # Pcap file
│   ├── 2018-08-08.19:50:16.pcap
│   ├── 2018-08-08.19:50:17.pcap
│   ├── 2018-08-08.19:50:18.pcap
│   └── 2018-08-08.19:50:19.pcap
├── 3fd3738e-0047-4584-87d1-0712ff02e786
│   ├── 2018-08-08.19:50:31.pcap
│   ├── 2018-08-08.19:50:32.pcap
│   ├── 2018-08-08.19:50:33.pcap
│   └── 2018-08-08.19:50:34.pcap
├── 8d70aa09-49a5-4679-870b-f3b25f7984db
│   ├── 2018-08-08.19:50:38.pcap
│   ├── 2018-08-08.19:50:39.pcap
│   ├── 2018-08-08.19:50:40.pcap
│   └── 2018-08-08.19:50:41.pcap
├── 91097447-77de-419f-ad65-880242e9b43b
│   ├── 2018-08-08.19:50:47.pcap
│   └── 2018-08-08.19:50:48.pcap
└── 9bbf092b-30a3-4dae-ab31-145e769b1738
    ├── 2018-08-08.19:50:52.pcap
        ├── 2018-08-08.19:50:53.pcap
            └── 2018-08-08.19:50:54.pcap

            5 directories, 18 files

```

