# Văn phong: viết cho giống người, bớt "mùi AI" (bản chọn lọc cho báo cáo học thuật)

Chắt lọc từ bộ quy tắc [humanizer](https://github.com/blader/humanizer) (dựa trên Wikipedia
"Signs of AI writing"). **Đã loại các quy tắc xung đột với văn phong học thuật** (giọng hội
thoại, ngôi thứ nhất, câu hỏi tu từ...). Áp dụng cho báo cáo LaTeX và mọi văn bản tiếng Việt
trong dự án.

## A. Quy tắc ÁP DỤNG

1. **Không thổi phồng.** Bỏ tính từ ca ngợi (đột phá, vượt trội, mạnh mẽ, vô cùng, to lớn,
   cách mạng). Nêu sự kiện/số liệu thay vì cảm thán.
2. **Bỏ phân tích rỗng.** Tránh "thể hiện/phản ánh/cho thấy/khẳng định" khi không kèm bằng
   chứng cụ thể.
3. **Động từ thẳng (copula).** Ưu tiên "là / có / gồm" thay cho "đóng vai trò quan trọng
   trong việc", "được xem là", "được coi như". Giữ "đóng vai trò" chỉ khi thật sự mô tả vai
   trò, và bỏ chữ "quan trọng" nhồi thừa.
4. **Bỏ song hành phủ định.** "không chỉ X mà còn Y" → nêu thẳng "X và Y" hoặc tách hai câu.
5. **Không ép bộ ba.** Liệt kê đúng số mục thực có, đừng cố cho đủ ba.
6. **Thuật ngữ nhất quán.** Lặp lại đúng từ khóa (vd "tầng Gold", "guardrails"), không xoay
   vòng từ đồng nghĩa cho "sang".
7. **Bỏ dải giả.** "từ X đến Y" khi không phải khoảng liên tục → liệt kê thẳng.
8. **Hạn chế gạch ngang dài (—).** Thay bằng dấu phẩy, chấm, hai chấm hoặc ngoặc đơn.
9. **Chữ đậm có chừng mực.** `\textbf` chỉ cho thuật ngữ định nghĩa lần đầu, không bôi đậm tràn lan.
10. **Cắt từ đệm.** "nhằm mục đích" → "để"; "một cách \textit{[tính từ]}" → bỏ "một cách";
    "trong việc" → bỏ khi thừa. Dùng "do đó / vì vậy / nhờ đó / bên cạnh đó" vừa phải, không lặp.
11. **Bớt rào đón.** Gộp "có thể có khả năng" → "có thể". Bỏ "nhìn chung, về cơ bản, nói chung"
    khi rỗng nghĩa.
12. **Kết luận cụ thể.** Không "mở ra nhiều triển vọng to lớn"; nêu kết quả, số liệu, hoặc
    hướng phát triển cụ thể.
13. **Vào thẳng vấn đề.** Bỏ mở đầu sáo: "Trong thời đại ngày nay", "Có thể nói rằng",
    "Về cơ bản/Về bản chất", "Đi sâu vào".
14. **Đa dạng nhịp câu.** Tránh chuỗi câu cùng độ dài/cấu trúc; trộn câu ngắn và dài.
15. **(Doc/commit/chat)** Không artifact chatbot ("Hy vọng giúp ích"), không nịnh, không hỏi
    "bạn có muốn..." thừa. Mô tả *chức năng*, không mô tả "đã đổi gì".

## B. Danh sách "mùi AI" tiếng Việt — bỏ hoặc hạn chế
đột phá · vượt trội · mạnh mẽ · vô cùng · to lớn · cách mạng · đáng chú ý là · nhìn chung ·
về cơ bản · về bản chất · trong thời đại ngày nay · có thể nói rằng · không thể phủ nhận ·
đóng vai trò quan trọng · một cách \textit{[tính từ]} · nhằm mục đích · mở ra triển vọng ·
tiềm năng to lớn · không chỉ... mà còn · hơn nữa/bên cạnh đó (lặp nhiều) · thể hiện/phản ánh (rỗng).

## C. KHÔNG áp dụng (ngoại lệ học thuật — quan trọng)
- **Ngôi:** humanizer khuyến khích giọng cá nhân/nêu chủ thể; báo cáo **giữ ngôi trung tính,
  KHÔNG "tôi/chúng tôi/em"**. Chủ ngữ là "đồ án / hệ thống / nghiên cứu" — chấp nhận.
- **Giọng hội thoại, câu hỏi tu từ, mở đầu thân mật:** không dùng trong báo cáo.
- **Bị động:** tiếng Việt học thuật chấp nhận câu không nêu chủ thể khi tự nhiên; không ép
  "nêu tên chủ thể" nếu làm câu kém trang trọng.
- **Quy ước tiếng Anh** (tiêu đề viết thường, bỏ gạch nối, dấu nháy thẳng, bỏ emoji): emoji thì
  bỏ; còn lại không bắt buộc cho tiếng Việt.

## D. Quy trình 2 lượt
1. Viết đúng nội dung và số liệu trước (số phải đã kiểm chứng — xem HANDOFF §4).
2. Đọc lại, tự hỏi *"đoạn này có vẻ do AI viết không?"*, soát theo mục A–B, rồi sửa. Không đụng
   bảng/hình/`\label`/`\ref`/`\cite`/số liệu.
