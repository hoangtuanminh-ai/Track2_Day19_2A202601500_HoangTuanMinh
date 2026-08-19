# Reflection — Lab 19

**Tên:** _Hoàng Tuấn Minh_
**Cohort:** _2A202601500_
**Path đã chạy:** _lite_

---

## Câu hỏi (≤ 200 chữ)

> Trên golden set 50 queries, mode nào thắng ở loại query nào (`exact` /
> `paraphrase` / `mixed`), và tại sao? Khi nào bạn **không** dùng hybrid
> (i.e. khi nào pure BM25 hoặc pure vector là lựa chọn đúng)?

- **Exact**: Keyword (BM25) thường chiếm ưu thế do khả năng khớp chính xác các từ khóa, mã số, hoặc tên riêng mà không bị "ảo giác" ngữ nghĩa.
- **Paraphrase**: Semantic (Vector) thắng nhờ khả năng hiểu nghĩa của từ và cụm từ tương đương, dù người dùng không dùng đúng từ khoá trong tài liệu.
- **Mixed**: Hybrid thắng do kết hợp được thế mạnh của cả hai qua thuật toán Reciprocal Rank Fusion (RRF).

**Không dùng hybrid khi:** 
1. Cần tối ưu chi phí và độ trễ (latency), vì hybrid phải chạy cả 2 luồng truy vấn.
2. Khi domain tìm kiếm quá đặc thù chỉ toàn mã ID, SKU, Log (nên dùng BM25).

---

## Điều ngạc nhiên nhất khi làm lab này

Cấu hình để chạy Lite (In-memory cho Qdrant/Feast) rất mượt, việc chuyển đổi qua lại giữa file `.py` và `.ipynb` thông qua Jupytext giúp cho việc xem xét, lưu giữ tiến độ và review code rất thuận tiện mà không bị mất mát code logic.

---

## Bonus challenge

- [ ] Đã làm bonus (xem `bonus/`)
- [ ] Pair work với: _<tên đồng đội nếu có>_
