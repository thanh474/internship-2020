### Task
Viết 1 file bash input là 1 cidr bất kỳ, yêu cầu tìm ra các host alive trong dải mạng đấy và OS của chúng.
ex: 
~> bash run.sh 192.168.1.0/22
Host 192.168.1.2 alive and using linux
Host 192.168.1.27 alive and using Windows
Done.
Total run in 73 sec

### Demo 
![](https://github.com/linhnt31/internship-2020/blob/linhnt-baocao-t1/LinhNT/Task-1-Find-all-hosts-alive/demo.png)

> Để chạy script ta sử dụng

```
sudo bash script.sh
```

OR

```
./script.sh
```

Command-line thứ 2 yêu cầu cấp quyền để **execute** 
> sudo chmod +x script.sh
### Cons 
1. Hiện tại chỉ đọc được 2 OSs là: Linux, Window, others : "unknown"
2. Mới giải quyết các dải mạng thuộc lớp C.
3. **nmap** phải quét 64000 ports (số lượng quá nhiều) , nhiều khi timeout được set quá ngắn để nmap có thể kịp detect ( Fixed by using TTL to detect) 

### Reference
https://www.cyberciti.biz/faq/mapping-lan-with-linux-unix-ping-command/

https://blog.opensistemas.com/how-to-find-alive-hosts-in-our-network/

https://nmap.org/book/osdetect-usage.html

https://www.cyberciti.biz/tips/simple-linux-and-unix-system-monitoring-with-ping-command-and-scripts.html

https://vinasupport.com/cach-su-dung-lenh-grep-trong-linux/

https://www.reddit.com/r/linuxadmin/comments/3olh4k/bash_increment_first_octet_by_1/

https://www.cyberciti.biz/faq/bash-shell-find-out-if-a-variable-has-null-value-or-not/

https://www.cyberciti.biz/faq/how-to-assign-a-grep-command-value-to-a-variable-in-linuxunix/

https://www3.ntu.edu.sg/home/ehchua/programming/howto/Regexe.html

https://dev.to/ankitdobhal/operating-system-detection-using-ttl-value-powershell-ping-51l8
