# Giải thích siêu dễ hiểu: game Hand Catch

## 1. Game là gì?

Giống trò **hứng trứng**: ở dưới màn hình có một cái giỏ. Bạn **đưa tay sang trái thì giỏ chạy sang trái, đưa tay sang phải thì giỏ chạy sang phải**.

- 🔴 Quả đỏ rơi xuống: hứng được thì **+10 điểm**, để rơi thì **mất 1 mạng**.
- 🟡 Ngôi sao: hứng được thì **+50 điểm**.
- 🟣 Bom: hứng trúng thì **mất 1 mạng**.
- Có 3 mạng. Được **1500 điểm là thắng**, hết mạng là thua.

Bạn còn có thể ra lệnh bằng **số ngón tay**:

| Giơ | Làm gì |
|---|---|
| ✋ 5 ngón | Bắt đầu / chơi tiếp |
| ✊ 0 ngón (nắm tay) | Tạm dừng |
| ☝️ 1 ngón | Đồ rơi chậm lại |
| ✌️ 2 ngón | Giỏ to gấp đôi |
| 3 ngón | Khiên: đỡ giúp 1 lần mất mạng |
| 4 ngón | Xoá hết bom |

## 2. Máy tính làm gì? (chỉ có 4 bước)

Máy tính làm đi làm lại 4 bước này, khoảng **30 lần mỗi giây**:

1. **Chụp** một tấm ảnh từ camera.
2. **Tìm tay**: MediaPipe nhìn ảnh và chấm **21 cái chấm** lên bàn tay.
3. **Đọc tay**: code của mình xem tay đang ở đâu, và đang giơ mấy ngón.
4. **Chơi và vẽ**: cho đồ rơi xuống một chút, xem có rơi vào giỏ không, rồi vẽ lên màn hình.

## 3. 21 cái chấm trên bàn tay

```
        8   12  16  20      ← đầu ngón
        7   11  15  19
   4    6   10  14  18      ← khớp giữa ngón
   3    5    9  13  17
   2
   1
            0               ← cổ tay
```

MediaPipe chỉ cho mình **vị trí 21 chấm** này. Còn "tay đang giơ mấy ngón" thì **mình tự đếm**.

## 4. Các "thuật toán" (thật ra rất dễ)

### 4.1. Giỏ đi theo tay

Mình lấy chấm số **9** (ở giữa lòng bàn tay) để biết tay đang ở đâu.

Nếu giỏ nhảy ngay tới chỗ tay thì nó sẽ **rung rung** (vì các chấm hơi nhúc nhích). Nên mình cho giỏ **mỗi lần chỉ đi 1/3 quãng đường** tới tay:

```python
basket_x += (hand_x - basket_x) / 3
```

Ví dụ: giỏ ở 0, tay ở 90 → lần 1 giỏ tới 30, lần 2 tới 50, lần 3 tới 63... cứ thế đuổi theo tay một cách êm ái.

### 4.2. Đếm ngón tay

Mẹo: **ngón duỗi thẳng thì đầu ngón ở xa cổ tay. Ngón gập lại thì đầu ngón quay về gần cổ tay.**

Với mỗi ngón, mình so 2 khoảng cách:
- từ **đầu ngón** tới cổ tay,
- từ **khớp giữa ngón** tới cổ tay.

Đầu ngón **xa hơn** khớp → ngón đang **giơ**. Đếm 1.

Ngón cái thì gập ngang, nên mình so khoảng cách tới **gốc ngón út** (chấm 17) thay vì cổ tay. Ý tưởng y hệt.

```python
for tip, joint in [(8, 6), (12, 10), (16, 14), (20, 18)]:
    if distance(points[tip], wrist) > distance(points[joint], wrist):
        count += 1
```

### 4.3. Phải giữ yên mới tính

Nếu vừa thấy 0 ngón là tạm dừng liền, thì lúc vẫy tay nhanh game sẽ dừng lung tung.

Nên mình **đếm xem cùng một số ngón đã được thấy bao nhiêu lần liên tiếp**. Đủ **15 lần** (khoảng nửa giây) mới làm theo. Đổi số ngón là đếm lại từ 1.

Nếu **không thấy tay 45 lần liên tiếp** (khoảng 1.5 giây) thì game tự tạm dừng.

### 4.4. Có hứng được không?

Khi một món đồ rơi tới **ngang tầm cái giỏ**:
- nếu nó nằm **trong bề ngang của giỏ** → hứng được,
- nếu không → rơi mất.

```python
if abs(thing["x"] - self.basket_x) <= half:
```

(`half` là nửa bề ngang giỏ. Khoảng cách từ món đồ tới giữa giỏ nhỏ hơn nửa giỏ thì là nằm trong giỏ.)

### 4.5. Đồ rơi

Mỗi lần lặp, mỗi món đồ **tụt xuống vài pixel**. Điểm càng cao thì **level** càng cao (cứ 300 điểm lên 1 level), đồ rơi càng nhanh và xuất hiện càng dày.

Đồ mới được chọn ngẫu nhiên: **20% là bom, 7% là sao, còn lại là quả**.

### 4.6. Kỹ năng

Mỗi kỹ năng tốn **5 năng lượng**. Hứng quả được +1, hứng sao được +3, tối đa 10.

- **1 ngón – chậm:** tốc độ rơi chia đôi trong 150 lần lặp (khoảng 5 giây).
- **2 ngón – giỏ to:** bề ngang giỏ nhân đôi trong 180 lần lặp (khoảng 6 giây).
- **3 ngón – khiên:** bật một "công tắc". Lần mất mạng tiếp theo, nếu công tắc đang bật thì tắt nó đi thay vì trừ mạng.
- **4 ngón – xoá bom:** bỏ hết bom ra khỏi danh sách đồ đang rơi.

## 5. Mỗi file làm gì?

| File | Nói nôm na |
|---|---|
| `main.py` | **Nhạc trưởng**: mở camera, gọi các file khác, vẽ lên màn hình |
| `hand.py` | **Đôi mắt**: dùng MediaPipe tìm 21 chấm, rồi đếm ngón |
| `game.py` | **Luật chơi**: đồ rơi, hứng, điểm, mạng, kỹ năng |
| `test_game.py` | **Kiểm tra bài**: tự chạy thử để chắc code đúng |

## 6. Nếu thầy/cô hỏi

- **MediaPipe làm gì?** Tìm 21 chấm trên bàn tay trong ảnh. Chỉ vậy thôi.
- **Em tự làm gì?** Cho giỏ đi theo tay, đếm ngón tay, bắt phải giữ yên mới tính, kiểm tra hứng được hay không, tính điểm, mạng, level và 4 kỹ năng.
- **Đếm ngón thế nào?** Đầu ngón xa cổ tay hơn khớp giữa ngón thì ngón đang giơ.
- **Sao giỏ không rung?** Vì mỗi lần giỏ chỉ đi 1/3 quãng đường tới tay.
- **Sao không bị tạm dừng nhầm?** Vì phải thấy cùng số ngón 15 lần liên tiếp.
