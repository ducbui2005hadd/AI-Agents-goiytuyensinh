
import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

def train_and_save_vietnamese_model():
    """
    Trains a new TF-IDF model from the translated Vietnamese data and saves it.
    """
    print("Bắt đầu huấn luyện mô hình tiếng Việt...")
    
    try:
        final_df = pd.read_csv('final_majors_data_vi.csv')
        final_df['major_description_vi'] = final_df['major_description_vi'].fillna('')
        print("✅ Đã tải dữ liệu 'final_majors_data_vi.csv' thành công.")
    except FileNotFoundError:
        print("❌ Lỗi: Không tìm thấy tệp 'final_majors_data_vi.csv'. Vui lòng chạy tệp 'translate_data.py' trước.")
        return None, None, None

    # Train TF-IDF on the Vietnamese description
    vectorizer = TfidfVectorizer(max_features=1000)
    major_vectors = vectorizer.fit_transform(final_df['major_description_vi'])
    
    # Save the new vectorizer and the vectors
    joblib.dump(vectorizer, 'tfidf_vectorizer_vi.pkl')
    joblib.dump(major_vectors, 'major_vectors_vi.pkl')
    
    print("✅ Huấn luyện và lưu mô hình tiếng Việt thành công ('tfidf_vectorizer_vi.pkl', 'major_vectors_vi.pkl').")
    return vectorizer, major_vectors, final_df

def get_recommendations_vi(user_interest, min_score=60, top_n=5):
    """
    Gets recommendations based on a Vietnamese user query.
    """
    print(f"\n🔍 Tìm kiếm cho: '{user_interest}' (điểm đại học tối thiểu: {min_score})")
    print("-" * 70)

    # Load the Vietnamese model and data
    try:
        vectorizer = joblib.load('tfidf_vectorizer_vi.pkl')
        major_vectors = joblib.load('major_vectors_vi.pkl')
        final_df = pd.read_csv('final_majors_data_vi.csv')
    except FileNotFoundError:
        print("⚠️ Không tìm thấy tệp mô hình hoặc dữ liệu tiếng Việt. Đang tiến hành huấn luyện lần đầu...")
        vectorizer, major_vectors, final_df = train_and_save_vietnamese_model()
        if vectorizer is None:
            return

    # Filter by score
    filtered_df = final_df[final_df['university_score'] >= min_score].copy()
    
    if filtered_df.empty:
        print("❌ Không có ngành học nào phù hợp với mức điểm tối thiểu.")
        return

    # Get the indices in the original dataframe that correspond to the filtered dataframe
    filtered_indices = filtered_df.index
    
    # Calculate similarities
    user_vector = vectorizer.transform([user_interest])
    # Filter the major_vectors to only include the vectors for the filtered schools
    filtered_major_vectors = major_vectors[filtered_indices]
    
    similarities = cosine_similarity(user_vector, filtered_major_vectors)
    
    # Add similarity scores to the filtered dataframe and get the top N
    filtered_df['similarity'] = similarities[0]
    recommendations = filtered_df.nlargest(top_n, 'similarity')
    
    if recommendations.empty:
        print("   Không tìm thấy kết quả phù hợp.")
        return

    print("🏆 CÁC KẾT QUẢ GỢI Ý HÀNG ĐẦU:")
    for idx, (_, row) in enumerate(recommendations.iterrows(), 1):
        print(f"\n{idx}. 🎓 {row['major_name_vi']}")
        print(f"   🏫 {str(row['university_name']).title()}")
        print(f"   ⭐ Điểm trường: {row['university_score']:.1f}")
        print(f"   💫 Độ phù hợp: {row['similarity']:.3f}")

if __name__ == '__main__':
    # --- BẠN CÓ THỂ THAY ĐỔI CÁC GIÁ TRỊ DƯỚI ĐÂY ĐỂ THỬ NGHIỆM ---
    
    # Nhập sở thích của bạn bằng tiếng Việt
    my_interest = "phân tích dữ liệu và học máy" 
    
    # Nhập điểm đầu vào tối thiểu của trường đại học
    min_university_score = 65
    
    # Nhập số lượng kết quả bạn muốn xem
    number_of_results = 3
    
    # --------------------------------------------------------------------
    
    get_recommendations_vi(my_interest, min_university_score, number_of_results)

    # Thử nghiệm với một trường hợp khác
    get_recommendations_vi("quản trị kinh doanh và marketing", 60, 3)
