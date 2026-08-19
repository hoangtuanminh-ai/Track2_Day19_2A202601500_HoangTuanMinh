# Hướng Dẫn Từng Bước Hoàn Thành Lab Day 19 Trên Windows (Lite Path)

Tài liệu này hướng dẫn chi tiết cách thiết lập, chạy thử nghiệm, chạy ứng dụng FastAPI và Jupyter Lab trên **hệ điều hành Windows** (native, không cần WSL hay Docker). Môi trường được cấu hình theo **Lite Path** chạy hoàn toàn in-memory và sử dụng SQLite làm Online Store cho Feast, tối ưu hóa RAM (~700MB) và cài đặt cực kỳ nhanh chóng.

---

## 🛠️ Yêu cầu hệ thống
*   **Python:** Phiên bản từ `3.10` đến `3.14` (Máy của bạn hiện có **Python 3.13.1** - Hoàn hảo).
*   **uv (Khuyên dùng):** Công cụ quản lý môi trường ảo siêu tốc (Máy của bạn hiện đã cài sẵn **uv 0.11.32** - Quá tuyệt vời!).
*   **Shell sử dụng:** Hướng dẫn này hỗ trợ cả **PowerShell** và **Command Prompt (CMD)** của Windows.

---

## 🚀 Bước 1: Khởi Tạo Môi Trường Ảo (Virtual Environment)
Mở PowerShell hoặc Command Prompt (CMD) tại thư mục gốc của dự án (`d:\AI2OK_LAB\1. DAY 19\Track2_Day19_2A202601500_HoangTuanMinh`), thực hiện các lệnh sau:

### Cách 1: Sử dụng `uv` (Khuyên dùng - Cực nhanh chỉ ~2 giây)
```powershell
# Tạo môi trường ảo .venv
uv venv .venv

# Kích hoạt môi trường ảo (Chọn lệnh phù hợp với shell của bạn)
# Nếu dùng PowerShell (BẮT BUỘC phải có dấu chấm và dấu cách ở đầu để kích hoạt ở shell hiện tại - Dot-Sourcing):
. .venv\Scripts\Activate.ps1
# Nếu dùng CMD (Command Prompt):
.venv\Scripts\activate.bat
```

### Cách 2: Sử dụng Python venv truyền thống
```powershell
# Tạo môi trường ảo .venv
python -m venv .venv

# Kích hoạt môi trường ảo
# Nếu dùng PowerShell (BẮT BUỘC phải có dấu chấm và dấu cách ở đầu - Dot-Sourcing):
. .venv\Scripts\Activate.ps1
# Nếu dùng CMD (Command Prompt):
.venv\Scripts\activate.bat
```

> [!TIP]
> **Lưu ý trên PowerShell:** Nếu gặp lỗi bảo mật `Script Execution Policy` ngăn cản kích hoạt venv, hãy chạy lệnh sau trước rồi thử kích hoạt lại:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
> ```

---

## 📦 Bước 2: Cài Đặt Dependencies (Thư Viện Phụ Thuộc)
Sau khi kích hoạt môi trường ảo (đầu dòng terminal hiển thị dấu `(.venv)`), hãy tiến hành cài đặt các thư viện cần thiết:

### Cách 1: Sử dụng `uv` (Siêu tốc ~15 giây)
```powershell
uv pip install -r requirements.txt
```

### Cách 2: Sử dụng `pip` truyền thống
```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

## 🔄 Bước 3: Chuyển Đổi Jupytext (.py) sang Jupyter Notebook (.ipynb)
Vì các notebook trong bài Lab được lưu dưới dạng file Python script `.py` (định dạng Jupytext để dễ kiểm soát phiên bản), bạn cần chuyển đổi chúng sang định dạng `.ipynb` để làm việc trên Jupyter Lab.

Chạy lệnh Python độc lập dưới đây (hoạt động tốt trên cả CMD và PowerShell, tránh lỗi wildcard `*` của shell Windows):
```powershell
.venv\Scripts\python -c "import glob, subprocess; [subprocess.run(['.venv/Scripts/jupytext', '--to', 'notebook', '--update', f]) for f in glob.glob('notebooks/[0-9]*.py')]"
```

---

## ⚙️ Bước 4: Tạo Tệp Cấu Hình Môi Trường `.env`
Sao chép tệp mẫu cấu hình môi trường `.env.example` thành `.env`.

*   **Nếu dùng PowerShell:**
    ```powershell
    if (-not (Test-Path .env)) { Copy-Item .env.example .env }
    ```
*   **Nếu dùng CMD (Command Prompt):**
    ```cmd
    if not exist .env copy .env.example .env
    ```

---

## 📊 Bước 5: Sinh Dữ Liệu Mẫu Và Chạy Smoke Test
Chạy lần lượt các script để tạo cơ sở dữ liệu mẫu tiếng Việt, các truy vấn phục vụ bài nâng cao và chạy kiểm tra nhanh (smoke test) xem môi trường đã sẵn sàng chưa:

```powershell
# 1. Sinh 1000 tài liệu tiếng Việt và 50 golden queries
python scripts/seed_corpus.py

# 2. Sinh dữ liệu nâng cao cho NB6 & NB8
python scripts/gen_agent_queries.py
python scripts/gen_spend.py

# 3. Chạy Smoke Test kiểm tra hệ thống (Phải in ra "All checks passed")
python scripts/verify_lite.py
```

---

## 🌐 Bước 6: Khởi Động FastAPI Server (Background API)
Bài Lab yêu cầu chạy FastAPI ở cổng `8000` để phục vụ tìm kiếm Hybrid Search qua REST API.

1.  **Mở một cửa sổ Terminal mới** (CMD hoặc PowerShell).
2.  Di chuyển đến thư mục dự án.
3.  Kích hoạt môi trường ảo:
    ```powershell
    .venv\Scripts\activate
    ```
4.  Khởi động server FastAPI:
    ```powershell
    uvicorn app.main:app --reload --port 8000
    ```
    *(Giữ nguyên cửa sổ này đang chạy để debug log và phục vụ benchmark)*

---

## 📓 Bước 7: Khởi Động Jupyter Lab Để Làm Bài
Cách tốt nhất trên Windows là gọi trực tiếp file thực thi trong môi trường ảo `.venv` (không lo lắng việc venv đã được kích hoạt thành công hay chưa):

```powershell
.venv\Scripts\jupyter lab --notebook-dir=notebooks --ServerApp.token="" --no-browser
```

Hoặc nếu bạn đã kích hoạt môi trường ảo thành công bằng cách Dot-Sourcing (`. .venv\Scripts\Activate.ps1`) ở Bước 1, bạn có thể chạy:

```powershell
jupyter lab --notebook-dir=notebooks --ServerApp.token="" --no-browser
```

Khi Terminal hiển thị các đường dẫn dạng URL, hãy sao chép một URL (ví dụ: `http://localhost:8888/...`) dán vào trình duyệt Web của bạn.
Bạn bắt đầu làm bài tuần tự từ tệp **`01_embeddings_index.ipynb`** đến **`08_feature_engineering.ipynb`**.

---

## 🏆 Hướng Dẫn Thực Hiện 8 Chặng Lab

### ⏱️ Chặng 1: Biến Văn Bản Thành Vector & Index Vào Qdrant (`01_embeddings_index.ipynb`) - 15 Điểm
*   **Nhiệm vụ:** Nạp 1.000 tài liệu tiếng Việt từ `data/corpus_vn.jsonl`, dùng `fastembed` (model `BAAI/bge-small-en-v1.5`) sinh dense vector 384 chiều, nạp vào collection `lab19` trên Qdrant in-memory kèm payload (`doc_id`, `topic`, `title`).
*   **Kết quả mong đợi:** Cell kiểm tra chạy qua xác nhận `client.count("lab19").count == 1000`. Query tìm kiếm bằng câu diễn đạt khác không chứa từ khóa "cloud" vẫn trả về các tài liệu thuộc chủ đề điện toán đám mây.
*   **Lưu ý:** Lần chạy đầu tiên sẽ mất khoảng 30s để tải model ONNX về máy.

### ⏱️ Chặng 2: Hybrid Search & Thuật Toán Ghép Điểm RRF (`02_hybrid_search_rrf.ipynb`) - 20 Điểm
*   **Nhiệm vụ:** Kết hợp BM25 (từ khóa chính xác) và Vector (ngữ nghĩa) theo công thức RRF chuẩn:
    $$\text{Score}(d) = \sum_{m \in \{\text{BM25}, \text{Vector}\}} \frac{1}{60 + \text{rank}_m(d)}$$
*   **[Quy tắc vàng]:** $\text{rank}$ bắt đầu từ **1** (1-based index). Tài liệu top-1 có mẫu số là $60 + 1 = 61$. Tuyệt đối không dùng 0-based index!
*   **Kết quả mong đợi:** Bảng `Precision@10` trung bình cho thấy kết quả: `Hybrid > BM25` và `Hybrid > Vector`.

### ⏱️ Chặng 3: Xây Dựng REST API & Đo Độ Trễ Server (`03_search_api_benchmark.ipynb`) - 15 Điểm
*   **Nhiệm vụ:** Hoàn thiện API endpoint `GET /search?q=...&mode=hybrid&top_k=10` tại file `app/main.py`. Đảm bảo response trả về có chứa trường thời gian phản hồi `latency_ms`.
*   **Kết quả mong đợi:** Chạy đo lường benchmark đạt yêu cầu `hybrid P99 server-side < 50ms`.
*   **Mẹo:** Gửi 5–10 request nháp để khởi động (warm-up) server tránh độ trễ do khởi động nguội (cold start).

### ⏱️ Chặng 4: Quản Lý Hồ Sơ Thực Thể Với Feast Feature Store (`04_feast_feature_store.ipynb`) - 20 Điểm
*   **Nhiệm vụ:**
    1. Định nghĩa 3 views (`user_profile`, `item_popularity`, `query_velocity`) trong `app/feast_repo/feature_views.py`.
    2. Chạy lệnh: `feast -c app/feast_repo apply` để đăng ký các view với registry.
    3. Chạy đồng bộ dữ liệu lịch sử sang SQLite Online Store: `feast -c app/feast_repo materialize-incremental <thời gian hiện tại>` (Ví dụ: `feast -c app/feast_repo materialize-incremental 2026-08-19T23:59:59`).
    4. Thực hiện truy xuất online (`get_online_features`) và PIT Join (`get_historical_features`).
*   **Kết quả mong đợi:** Online Lookup $P_{99} < 10\text{ms}$. PIT Join trả về DataFrame đúng 3 dòng khớp lịch sử không bị rò rỉ dữ liệu tương lai.

### ⏱️ Chặng 5: Vực Thẳm Chọn Lọc Trong Filtered Search (`05_filtered_search.ipynb`) - 8 Điểm
*   **Nhiệm vụ:** So sánh 3 chiến lược lọc tài liệu: Post-filter, Over-fetch và Filtered-ANN.
*   **Kết quả mong đợi:** Chứng minh Post-filter sập Recall về 0% khi điều kiện lọc quá khắt khe (~4%). Filtered-ANN của Qdrant luôn giữ vững 100% Recall.

### ⏱️ Chặng 6: Agentic Retrieval — Truy Xuất Như Một Tool (`06_agent_retrieval.ipynb`) - 10 Điểm
*   **Nhiệm vụ:** Tạo schema `SEARCH_TOOL`, chạy `RuleBasedPlanner` phân rã câu hỏi phức hợp thành các truy vấn đơn lẻ, sau đó gọi `build_context()` để ghép dữ liệu Feast + Qdrant.
*   **Kết quả mong đợi:** Agentic vượt trội Single-shot về Recall và tính cân bằng thông tin trong cùng một mức tài liệu thu hồi.

### ⏱️ Chặng 7: Semantic Cache & An Toàn Dữ Liệu Đa Tenant (`07_semantic_cache.ipynb`) - 7 Điểm
*   **Nhiệm vụ:** Thiết lập cache tương đồng ngữ nghĩa, quét ngưỡng similarity threshold, và sửa lỗ hổng rò rỉ dữ liệu đa người dùng (OWASP LLM08) bằng cách nhúng `tenant_id` vào cache key namespace.

### ⏱️ Chặng 8: Feature Engineering & Rò Rỉ Dữ Liệu (`08_feature_engineering.ipynb`) - 5 Điểm
*   **Nhiệm vụ:** Chứng minh rò rỉ Target Encoding làm AUC ảo tăng vọt lên 0.99. Sửa lại bằng cách tính in-fold. Định nghĩa một On-Demand Feature View tính toán đặc trưng động tại runtime.

---

## 🧪 Bước 8: Kiểm Thử Tự Động Trước Khi Nộp Bài (Thay thế Makefile)
Trước khi commit bài làm để nộp, hãy chạy lần lượt 4 lệnh nghiệm thu sau trên Terminal đã kích hoạt venv để đảm bảo tất cả đều đạt chuẩn:

1.  **Kiểm tra toàn diện môi trường (Smoke Test):**
    ```powershell
    python scripts/verify_lite.py
    ```
2.  **Chạy bộ unit tests của repo:**
    ```powershell
    pytest -q
    ```
3.  **Chạy benchmark đo lường Precision@10 và độ trễ P99:**
    ```powershell
    python scripts/benchmark.py
    ```
4.  **Kiểm tra chạy sạch toàn bộ notebooks (Mô phỏng Grader chấm điểm):**
    ```powershell
    python scripts/run_notebooks_win.py
    ```

> [!NOTE]
> Khi tất cả các lệnh trên đều trả về kết quả **PASS** hoặc **All checks passed**, bài làm của bạn đã sẵn sàng 100% để nộp!

---

## 🛠️ Một Số Lỗi Thường Gặp Trên Windows (Troubleshooting)

| Triệu chứng | Nguyên nhân & Cách khắc phục |
| :--- | :--- |
| **Lỗi `jupyter` không nhận diện được (not recognized)** | Do bạn chạy trực tiếp `.venv\Scripts\Activate.ps1` trên PowerShell khiến script chạy ở scope con và chưa thực sự kích hoạt venv ở terminal chính. Cách sửa: Chạy lại bằng Dot-Sourcing: `. .venv\Scripts\Activate.ps1` (có dấu chấm và dấu cách ở đầu), hoặc chạy trực tiếp bằng đường dẫn đầy đủ `.venv\Scripts\jupyter lab ...`. |
| **Lỗi `feast` không nhận diện được khi chạy notebook** | Notebook thực thi Feast thông qua terminal. Đảm bảo bạn đã khởi chạy Jupyter Lab từ terminal đã kích hoạt venv, hoặc file `notebooks/_setup.py` sẽ tự động cấu hình đưa đường dẫn venv vào PATH. Nếu vẫn lỗi, thử xóa file registry cũ: `del app\feast_repo\registry.db` và chạy lại `feast apply`. |
| **Lỗi `port 8000 in use` khi khởi chạy FastAPI** | Cổng 8000 đang bị chiếm dụng bởi ứng dụng khác. Hãy tắt ứng dụng đó hoặc đổi cổng khi chạy uvicorn: `uvicorn app.main:app --reload --port 8001` (và nhớ cập nhật URL gọi API trong notebook 03 sang `http://localhost:8001`). |
| **Lỗi thư viện `pyarrow` hoặc `dill` crash** | Do phiên bản Python mới (ví dụ Python 3.14). Hãy chạy lệnh nâng cấp độc lập: `pip install --upgrade "dill>=0.4,<1.0"`. |
| **Lỗi không kết nối được Qdrant** | Đảm bảo bạn đang chạy ở chế độ Lite (`QDRANT_MODE=memory` trong file `.env`). Chế độ này không cần chạy Docker Qdrant Server. |
