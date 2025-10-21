
import pandas as pd
from deep_translator import GoogleTranslator
import time
import os

# Check if the translated file already exists
if os.path.exists('final_majors_data_vi.csv'):
    print("✅ Tệp 'final_majors_data_vi.csv' đã tồn tại. Bỏ qua bước dịch.")
else:
    print("Đã đọc tệp final_majors_data.csv. Bắt đầu quá trình dịch...")

    # Read the data
    try:
        df = pd.read_csv('final_majors_data.csv')
        print(f"Đã tải thành công {len(df)} dòng dữ liệu.")
    except FileNotFoundError:
        print("❌ Lỗi: Không tìm thấy tệp 'final_majors_data.csv'.")
        exit()

    # Initialize translator
    translator = GoogleTranslator(source='en', target='vi')

    # Prepare lists to hold translated data
    translated_names = []
    translated_descs = []

    print("Bắt đầu dịch tên ngành và mô tả. Quá trình này có thể mất vài phút...")

    # Iterate over the dataframe and translate
    for index, row in df.iterrows():
        try:
            # Translate major_name
            # Handle potential non-string data
            name_to_translate = str(row['major_name']) if pd.notna(row['major_name']) else ""
            translated_name = translator.translate(name_to_translate)
            translated_names.append(translated_name)

            # Translate major_description
            # Handle potential non-string data
            desc_to_translate = str(row['major_description']) if pd.notna(row['major_description']) else ""
            translated_desc = translator.translate(desc_to_translate)
            translated_descs.append(translated_desc)

            # Print progress
            if (index + 1) % 10 == 0:
                print(f"   ... đã dịch {index + 1}/{len(df)} dòng")
            
            # Add a small delay to avoid overwhelming the translation service
            time.sleep(0.1)

        except Exception as e:
            print(f"Lỗi ở dòng {index}: {e}")
            translated_names.append(row['major_name']) # Append original if translation fails
            translated_descs.append(row['major_description'])

    # Add new columns to the DataFrame
    df['major_name_vi'] = translated_names
    df['major_description_vi'] = translated_descs

    print("✅ Dịch thuật hoàn tất.")

    # Save the new dataframe to a new CSV file
    try:
        df.to_csv('final_majors_data_vi.csv', index=False, encoding='utf-8-sig')
        print("✅ Đã lưu thành công dữ liệu đã dịch vào tệp 'final_majors_data_vi.csv'.")
        print("\nNội dung tệp mới:")
        print(df[['major_name', 'major_name_vi', 'major_description_vi']].head())
    except Exception as e:
        print(f"❌ Lỗi khi lưu tệp: {e}")
