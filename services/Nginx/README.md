Basic Auth
```
printf "username:$(openssl passwd -crypt password)\n" >> ./auth/basic
```
