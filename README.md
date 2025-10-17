#  AI Agent Tư vấn Tuyển sinh

Đây là một project xây dựng AI Agent đơn giản để gợi ý ngành học đại học dựa trên điểm số và sở thích của người dùng.

##  Tính năng

-   Nhận đầu vào là điểm số và một chuỗi mô tả sở thích bằng tiếng Việt.
-   Tự động dịch sở thích sang tiếng Anh.
-   Sử dụng **Rule-based** để lọc các ngành phù hợp về điểm số.
-   Sử dụng **Machine Learning (TF-IDF & Cosine Similarity)** để xếp hạng các ngành theo độ phù hợp với sở thích.

##  Cách hoạt động

1.  **Chuẩn bị dữ liệu**: Kết hợp dữ liệu từ Kaggle (Coursera Courses & World University Rankings).
2.  **Xây dựng Model**: Huấn luyện mô hình TF-IDF trên mô tả các khóa học.
3.  **Gợi ý**: Lọc và xếp hạng để đưa ra top 5 gợi ý phù hợp nhất.
