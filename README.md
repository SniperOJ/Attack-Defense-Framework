Attack and Defense Framework
---

```
An Open Source CTF Attack and Defense Mode Framework
```

#### TODO
- [ ] websocket
- [ ] Manage server at web UI (webtty)
- [ ] Detect unusual flag submit (eg: every cycle flag is got from a specific team but wrong)
- [ ] HTTPS
- [ ] Auto deploy waf
- [ ] Auto send fake payloads
- [ ] Detect the health of official flag submit server
- [ ] Fix flag recovery
- [ ] Upgrade Railgun attack dispatching logic
- [ ] RSA webshell
- [ ] Mutliple flag regexp pattern
- [ ] Mutliple threads change ssh password
- [ ] SSH sessions management
- [ ] PWN shell session management (If no alarm)
- [x] OpenVPN
- [x] Webshell management
- [x] Railgun add cmdline paramters (sepcific challenge)
- [x] Search flag what if there are serval flag occurs in the response
- [x] Add priority too exploit
- [x] Keep attack until flag got in every cycle
- [x] Import targets from text file
- [x] Support for disable a specific exploit
- [x] Support for disable a specific target (team)
- [x] DNS server
- [x] nginx config generator
- [x] Config Django via config file

#### Installation
```
git clone git@github.com:SniperOJ/Attack-Defense-Framework.git
git checkout v2
git submodule update --init
```

#### Examples
> Fire Service  

![Image](https://upload-images.jianshu.io/upload_images/2355077-ee95171cdbf0d94d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

> Flag Service  

![Image](https://upload-images.jianshu.io/upload_images/2355077-280e23fbbe848ecd.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

> UI Service  

![Image](https://upload-images.jianshu.io/upload_images/2355077-c34fe47bf341698b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


#### Scripts

```
➜  utils git:(v2) ✗ tree
.
├── deamon
│   ├── bash.txt
│   ├── code.php
│   └── php.txt
├── flow
│   ├── out.port-forwarding.py
│   ├── patch-change-flag.py
│   ├── port-forwarding-change-flag.py
│   ├── port-forwarding.py
│   └── simple-port-multiplier.py
├── fs
│   ├── file_monitor.py
│   ├── sync
│   │   ├── README.md
│   │   ├── sync.sh
│   │   └── watch.py
│   └── watch.py
├── generator
│   └── iprange.py
├── php
│   ├── code_exec_bomb.py
│   ├── code_exec.py
│   ├── __init__.py
│   ├── shell_exec_bomb.py
│   └── shell_exec.py
└── ssh
    ├── auto_ssh.py
    └── targets

7 directories, 21 files
```

#### Acknownledgement
* [haozigege@lancet](https://github.com/zhl2008/flag_service)

#### [LICENSE](https://github.com/WangYihang/Attack_Defense_Framework/blob/master/LICENSE)
```
GNU GENERAL PUBLIC LICENSE(Version 3, 29 June 2007)
```
