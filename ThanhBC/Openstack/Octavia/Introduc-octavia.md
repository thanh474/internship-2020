# Giới thiệu về Octavia.


## 1. Octavia là gì.


Octavia là một project trong openstack nó được thiết kế cho giải pháp câng bằng tải trong openstack.

Octavia được phát triển từ project Neutron LBaaS. Những khái niệm của nó được kế thừa và phát triển từ project Neutron LBaaS version 1 và version 2. Bắt đầu từ phiêm bản Openstack Liberty  LBaaS version 2 đã đưcọ tách ra thành 1 project mới là Octavia.

Octavia chịu tránh nhiệm cân bằng tải giữa các nhóm máy ảo, containner, bare metal server nhưng endpoint trên đưcọ gọi là amphorae nó được octavia quay vòng theo yêu cầu.

Cân bằng tải là điều cần thiết cho việc mở rộng quy mô và tính khả dụng đây là các tính năng quan trong nhất của bất kỳ cloud nào. Do đó octavia cũng dc xem như là 1 project core và octavia có thể sử dụng cho các project khác như sau:
- Nova: Quản lý vòng đời các amphora và xoay chuyển tài nguyên theo yêu cầu.
- Neutron: Thiết kế mạng  giữa amphorae, project và mạng external.
- Keystone: Xác thực đối với octavia API và để octavia xác thực với các project khác.
- Oslo : Giao tiếp giữa các octavia component.

## 2. Các thuật ngữ sử dụng trong octavia.
Khi phát triển octavia đã phát triển thêm các thuật ngữ để tránh sự nhầm lẫn

- Amphora: Máy ảo, containner, appliance  hoặc thiết bị thực hiện nhiệm vụ cân bằng tải trong hệ thống Octavia.
- Amphora Load Balancer Driver: Thành phần của bộ điều khiển tất cả các giao tiếp với amphorae. Trình điều khiển điêu khiển  với bộ điều khiển thông qua 1 lớp cơ sở chung và các phương thức, đồn thời nó chuyển chúng thành các lệnh điều khiển cho các phần mềm chạy trên các back-end  amphorae. Những giao tiếp này thực hiện trên LB network.
- Apolocation:  Đâylà thuật ngữ khi 2 hoặc nhiều amphorae không được định vị trên cùng 1 vật lý phần cứng thường là liên kết trong HA. Hoặc sử dụng  để mô tả nhiều bộ cân bằng tải không dc kết nối đến cùng 1 amphorae.
- Controller: Deamon có quyền truy cập vào tất cả các thành phần mạng trong LB và Openstack điều phối quản lý hoạt động của hệ thống cân bằng tải octavia. Bộ điều khiển sử dụng trình điều khiển trừu tượng  để giao tiếp với  nhiều thành phần khác trong openstack. Đây là thành phân quan trong nhất trong octavia.
- HAProxy : Phần mềm cân bằng tải được sử dụng triển khai tham chiếu các thành phần cho octavia. HAProxy processes chạy trên amphorae và sử lý các task  cho load balancing service.
- Health Moniter: Sử dụng  kiểm tra cho từng amphorae trong nhóm. Nó kiểm tra các members trong nhóm đc liên kết với nó và lưu vào trong database.
- LB network: là  mạng cân bằng tải. Mạng mà các bộ điều khiển  và các amphorae với nhau. Mạng này thường sử dụng cho nova và neutron network mà các drivers và các amphorae có thẻ kết nối đươc. mangy này không kết nối trực tiếp với các project core mà chỉ kết nối với octavia controller và các amphorae. 
- Listener : Đối tượng endpoint lắng nghe loadbalance port. Sử dụng UPD/TCP port, 
- Load Balancer: Miêu ta đối tượng  logical  group các listener đang nghe trên VIPs và liên kết 1 hoặc nhiều amphorae.
- VIP ( Virtual IP Address): Địa chỉ IP liên kết với bộ cân bằng tải. Trong cấu trúc liên kết có sắn trong octavia, VIP có thể được gán vào các amphorae và các giao thức lớp 2 Như CARP, VRRP, hoặc HSRP để đảm bảo tính khả dụng của nó. Trong cấu trúc lớp 3 địa chỉ VIP được chỉ định dòng định tuyến các gói tin đên amphorae sau đó yêu cầu cần bằng tải đến các thanh viên phía sau.

## 3 Tổng quan các thành phần trong octavia.

![](otimg/octavia-component-overview.svg)

Octavia phiên bản 4.0 bao gồm các thành phần chính sau:

- Amphorae là các máy ảo, container  hoặc bare metal servers riêng lẻ để thực hiện việc cung cấp các dịch vụ cân bằng tải cho các môi trường ứng dụng của người thuê. Trong phiên bản Octavia 0.8, việc triển khai tham chiếu của hình ảnh amphorae là một máy ảo Ubuntu chạy HAProxy.

- Controller là “bộ não” của Octavia. Nó bao gồm năm thành phần phụ, là các daemon riêng lẻ. Chúng có thể được chạy trên cơ sở hạ tầng back-end riêng biệt nếu muốn:

    - Bộ điều khiển API - Như tên của nó, thành phần con này chạy API của Octavia. Nó nhận các yêu cầu API, thực hiện vệ sinh đơn giản trên chúng và chuyển chúng đến bộ điều khiển qua bus nhắn tin Oslo.

    - Controller Worker - Thành phần con này nhận các lệnh API đã được khử trùng từ bộ điều khiển API và thực hiện các hành động cần thiết để đáp ứng yêu cầu API.

    - Health Manager  - Thành phần phụ này giám sát từng amphorae để đảm bảo chúng luôn hoạt động và khỏe mạnh. Nó cũng xử lý các sự kiện chuyển đổi dự phòng nếu amphorae bị lỗi bất ngờ.

    - Housekeeping Manager - Thành phần con này dọn dẹp các bản ghi cơ sở dữ liệu cũ (đã xóa), quản lý nhóm phụ tùng và quản lý việc luân chuyển chứng chỉ amphora.

    - Driver Agent - Tác nhân trình điều khiển nhận cập nhật trạng thái và thống kê từ trình điều khiển của nhà cung cấp.

- Octavia network: nó  không thể thực hiện những gì nó làm mà không thao tác với môi trường mạng. Amphorae được tạo ra với một giao diện mạng trên “mạng cân bằng tải” và chúng cũng có thể cắm trực tiếp vào tennant network  để tiếp cận các thành viên nhóm phụ, tùy thuộc vào cách người thuê triển khai bất kỳ dịch vụ cân bằng tải cụ thể nào.