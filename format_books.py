import json
from datetime import datetime

# 기존 books_20250522.json 파일 읽기
with open('books_20250522.json', 'r', encoding='utf-8') as f:
    original_data = json.load(f)

# 새로운 형식으로 변환
new_data = []
for idx, book in enumerate(original_data['books']):
    new_book = {
        "model": "books.book",
        "pk": idx,
        "fields": {
            "title": book['title'],
            "author": book['author'],
            "publisher": book['publisher'],
            "pub_date": book['pubDate'],
            "description": book['description'],
            "isbn": book['isbn13'],
            "cover_image": book['cover'],
            "category_name": book['categoryName'],
            "category_color": book['categoryColor'],
            "price": book['price']
        }
    }
    new_data.append(new_book)

# 새로운 JSON 파일로 저장
output_filename = "formatted_books.json"
with open(output_filename, 'w', encoding='utf-8') as f:
    json.dump(new_data, f, ensure_ascii=False, indent=2)

print(f"도서 정보가 {output_filename}에 저장되었습니다.")
print(f"총 {len(new_data)}권의 도서 정보가 변환되었습니다.")
