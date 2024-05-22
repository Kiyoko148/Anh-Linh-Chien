# Giới thiệu game:

- Anh Linh Chiến là một tựa game turn-based chiến đấu tự động được mô phỏng dựa trên hệ thống “pet” được gọi là Anh Linh của tựa game Revelation: Thiên Dụ nổi tiếng của nhà phát hành VNG, với 3 loại Tấn Công , Phòng Thủ và Trị Liệu. Sử dụng các loại Anh Linh khác nhau để cùng bản thân vượt qua vô vàn khó khăn, gian nan thử thách. Mỗi Anh Linh đều có sự độc đáo riêng về các hệ chiến đấu cùng với sự tiếp thêm sức mạnh cho Anh Linh đến từ “Hồn Khí” và “Thần Võ” giúp cho người chơi có thể trải nghiệm game với các Anh Linh của bản thân.

- Cơ chế: người chơi dùng nút mũi tên di chuyển để chọn một trong số các Anh Linh sẵn có để xuất chiến, nhấn phím BACKSPACE để hủy chọn Anh Linh hiện tại và ENTER để xác nhận Anh Linh đã chọn. Có thể bấm ESCAPE để trở về màn hình chính.

- Chiến đấu: Sau khi chọn Anh Linh sẽ chuyển sang màn hình chờ chiến đấu và sẽ bắt đầu sau 5s. Cơ chế chiến đấu là tự động với tốc độ cao, dựa vào các chỉ số Tấn Công, Phòng Thủ, HP và Trị Liệu của Anh Linh và kẻ địch để đưa ra kết quả cuối cùng. Phe ta luôn hành động trước.

- Anh Linh: Gồm 3 loại: R, SR, SSR. Mỗi loại 3 Anh Linh

- Chỉ số:

* Anh Linh loại Tấn Công và Phòng Thủ sẽ không có chỉ số trị liệu.
* Anh Linh loại Tấn Công và Trị Liệu sẽ bị giảm chỉ số phòng thủ.
* Anh Linh loại Phòng Thủ và Trị Liệu sẽ bị giảm chỉ số tấn công.
* Anh Linh loại Phòng Thủ được tăng chỉ số phòng thủ.
* Anh Linh loại Trị Liệu được tăng chỉ số HP.

- Hệ chiến đấu:

* Gồm có 5 hệ: Hỏa, Lôi, Thủy, Quang, Ám
* Hỏa khắc Lôi và bị Thủy khắc.
* Lôi khắc Thủy và bị Hỏa khắc.
* Thủy khắc Hỏa và bị Lôi khắc.
* Quang và Ám khắc chế lẫn nhau.
* Khi khắc chế sẽ gây thêm 1,5 lần sát thương và tương tự với bị khắc chế.

# Installation:

### Lưu ý nên chạy cmd dưới quyền admin

- 1 - Tải python phiên bản mới nhất
- 2 - Clone repo từ GitHub và di chuyển vào thư mục:

```
git clone https://github.com/Kiyoko148/Anh-Linh-Chien.git
cd <path ti your file>/Anh-Linh-Chien
```

- 3 - Tạo và kích hoạt môi trường ảo (virtual environment):

```
python -m venv venv
.\venv\Scripts\activate
```

- 4 - Cài đặt các thư viện cần thiết:

```
pip install -r requirements.txt
```

- 5 - Chạy project:

```
python main.py
```
