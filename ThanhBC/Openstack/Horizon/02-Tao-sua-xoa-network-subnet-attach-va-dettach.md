# Hướng dẫn tạo sửa xóa network trên dashboard.


Để tạo nework mới ta vào tab Project -> Network -> Networks.

![](hzimg/cre-net1.png)

Chọn Create Network 


![](hzimg/cre-net2.png)

Sau đó sẽ hiện thị lê 1 pop-up. Ta điền cac thông tin vào. Rồi chọn next.

![](hzimg/cre-net3.png)

Chọn tên subnet, network address và gateway. Rồi chọn next.

![](hzimg/cre-net4.png)

Sau đó chọn pool cho dhcp và dns cuôi cùng chọn create.


![](hzimg/cre-net5.png)

Vậy là ta dã tạo xong network kiểu self-service.


Tiếp đến ta sẽ attack network này vào VM.

Chọn VM dể attach thêm 1 card mạng vào.
Project -> Compute -> Instances 

![](hzimg/atk-net1.png)

Sau đó chọn network cân attach.

![](hzimg/atk-net2.png)

Sau đó chọn Attach create

![](hzimg/atk-net3.png)

Như ta đã thầy VM của chúng ta đã có 2 địa chỉ ip ứng với 2 dải mạng đã dc gắn vào.

#