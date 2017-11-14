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
│   │   ├── get_flag.py
│   │   ├── __init__.py
│   │   └── submit_flag.py
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
│   ├── auto_ssh.py # auto change ssh weak password of other teams, and get flag on the target server then submit them
│   └── targets
└── targets # define the targets to attack
```
