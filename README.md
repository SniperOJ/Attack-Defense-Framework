Attack and Defense Framework
---

```
An Open Source CTF Attack and Defense Mode Framework
```


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
├── README.md
├── simple-port-multiplier.py # Port Multiplier with HTTP / SSH
├── sources # fake_requests.py need it to build fake http requests
│   └── index.php
├── ssh
│   ├── auto_ssh.py # auto change ssh weak password of other teams
│   └── targets
└── targets # define the targets to attack
```

#### [LICENSE](https://github.com/WangYihang/Attack_Defense_Framework/blob/master/LICENSE)
```
GNU GENERAL PUBLIC LICENSE(Version 3, 29 June 2007)
```
