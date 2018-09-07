Attack and Defense Framework
---

```
An Open Source CTF Attack and Defense Mode Framework
```

#### Examples
Flag submit server

![Image](https://upload-images.jianshu.io/upload_images/2355077-9158e3a59ef809ac.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

#### Scripts

```
.
├── core
│   ├── exploit
│   │   ├── get_flag.py # Please rewrite the function : get_flag in this script
│   │   ├── __init__.py
│   │   └── submit_flag.py # Please rewrite the funtion : submit_flag in this script
│   ├── __init__.py
│   ├── obfs # fake http requests lib
│   │   ├── fake_payloads.py
│   │   ├── get_arg.py
│   │   └── __init__.py
│   └── php
│       ├── code_exec_bomb.py
│       ├── code_exec.py
│       ├── __init__.py
│       ├── shell_exec_bomb.py
│       └── shell_exec.py
├── deamon # Dual process daemon Webshell
│   ├── bash.txt
│   ├── code.php
│   └── php.txt
├── exploit_all.py # Exploit all the gameboxes
├── fake_requests.py # Fake http requests
├── LICENSE
├── port-forwarding.py
├── watch.py # Web Directory Monitor via pyinotify
├── README.md
├── simple-port-multiplier.py # Port Multiplier with HTTP / SSH
├── sources # fake_requests.py need it to build fake http requests
│   └── index.php
├── ssh
│   ├── auto_ssh.py # auto change ssh weak password of other teams
│   └── targets
└── targets # define the targets to attack
```

#### Acknownledgement
* [haozigege@lancet](https://github.com/zhl2008/flag_service)

#### [LICENSE](https://github.com/WangYihang/Attack_Defense_Framework/blob/master/LICENSE)
```
GNU GENERAL PUBLIC LICENSE(Version 3, 29 June 2007)
```
