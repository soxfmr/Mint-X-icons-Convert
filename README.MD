#Mint-X-icons-Convert
Mint-X-icons-Convert is a tool which that porting the Mint-X-icons theme of Linux Mint to GNOME for Debian.

#How to use
You can download the Mint-X-icons via [https://github.com/linuxmint/mint-x-icons](https://github.com/linuxmint/mint-x-icons)

1) After modify the directory information of the icon, execute the checkout.py on shell:
```
./checkout.py
```

2) Copy the icon theme to the system, the command below should be run as administrator:
```
mkdir -p /usr/share/icons/Rootkit
cp -R Rootkit/* /usr/share/icons/Rootkit
```

3) Change the theme via gnome-tweak-tool

All done, Enjoy it! :)

#Snapshot
![](http://i13.tietuku.com/b10b7e4642c402a4.png)
