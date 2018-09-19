Basic Auth
```
mkdir /etc/nginx/auth
printf "username:$(openssl passwd -crypt password)\n" >> /etc/nginx/auth/basic
```
