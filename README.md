# Hand Catch – Game hứng đồ bằng bàn tay (MediaPipe Hand)

Đứng trước webcam, đưa tay sang trái hoặc phải để điều khiển cái giỏ, hứng trái cây và ngôi sao, tránh bom.

## Cài đặt và chạy

Cần Python 3.9–3.12 và một webcam.

```bash
pip install -r requirements.txt
python main.py
```

Nhấn `Q` hoặc `ESC` để thoát. Model `models/hand_landmarker.task` đã có sẵn trong thư mục.

## Cách chơi

| Làm gì | Kết quả |
|---|---|
| Đưa tay sang trái/phải | Giỏ chạy theo tay |
| Giơ 5 ngón (xoè tay) | Bắt đầu / chơi tiếp / về menu |
| Nắm tay (0 ngón) | Tạm dừng |
| Giơ 1 ngón | Làm chậm: đồ rơi chậm một nửa trong 5 giây |
| Giơ 2 ngón | Giỏ to gấp đôi trong 6 giây |
| Giơ 3 ngón | Khiên: đỡ giúp 1 lần mất mạng |
| Giơ 4 ngón | Xoá hết bom trên màn hình |
| Đưa tay ra khỏi camera 1.5 giây | Tự tạm dừng |

Mỗi cử chỉ phải giữ yên khoảng nửa giây mới được tính.

- Trái cây (đỏ): +10 điểm, +1 năng lượng. Để rơi thì mất 1 mạng.
- Ngôi sao (vàng): +50 điểm, +3 năng lượng.
- Bom (tím): hứng trúng thì mất 1 mạng.
- Mỗi kỹ năng 1–4 ngón tốn 5 năng lượng (tối đa 10).
- Có 3 mạng. Đạt 1500 điểm là thắng, hết mạng là thua. Điểm càng cao thì đồ rơi càng nhanh và càng dày.

## Các file

| File | Làm gì |
|---|---|
| `main.py` | Mở camera, gọi các phần khác, vẽ lên màn hình |
| `hand.py` | Dùng MediaPipe tìm 21 điểm trên bàn tay và đếm số ngón đang giơ |
| `game.py` | Luật chơi: đồ rơi, hứng, điểm, mạng, kỹ năng |
| `test_game.py` | Kiểm tra tự động: `python -m unittest test_game` |
| `docs/` | Giải thích code, hình minh hoạ |

## Thư viện

- [MediaPipe Hand Landmarker](https://developers.google.com/edge/mediapipe/solutions/vision/hand_landmarker)
- OpenCV

## Video demo

Link video demo: _(điền link sau khi quay)_
