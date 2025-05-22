import requests
import json
from datetime import datetime
import time

# 알라딘 API 설정
TTB_KEY = "ttbjungi29041414002"  # 여기에 발급받은 TTB 키를 입력하세요
BASE_URL = "http://www.aladin.co.kr/ttb/api/ItemList.aspx"

# 이미지에서 제공된 카테고리와 HEX 코드 매핑
CATEGORIES = {
    "로맨스": {"color": "#FF9AA2", "query_type": "ItemNewAll", "category_id": "50921"},  # 로맨스 소설
    "판타지/무협": {"color": "#B5A1DD", "query_type": "ItemNewAll", "category_id": "50926"},  # 판타지
    "추리/스릴러": {"color": "#355C7D", "query_type": "ItemNewAll", "category_id": "50922"},  # 추리/미스터리 소설
    "공포": {"color": "#23272A", "query_type": "ItemNewAll", "category_id": "50923"},  # 공포/호러 소설
    "사회/문화": {"color": "#BCAAA4", "query_type": "ItemNewAll", "category_id": "798"},  # 사회/문화
    "예술/대중문화": {"color": "#A7C7E7", "query_type": "ItemNewAll", "category_id": "517"},  # 예술/대중문화
    "시/문학": {"color": "#D6CDEA", "query_type": "ItemNewAll", "category_id": "1"},  # 시/문학
    "과학/기술": {"color": "#61C0BF", "query_type": "ItemNewAll", "category_id": "987"},  # 과학/기술
    "역사": {"color": "#8B3A3A", "query_type": "ItemNewAll", "category_id": "74"},  # 역사
    "인문/철학": {"color": "#7B8D8E", "query_type": "ItemNewAll", "category_id": "656"},  # 인문/철학
    "정신분석/심리": {"color": "#FFA64D", "query_type": "ItemNewAll", "category_id": "798"},  # 정신분석/심리
    "아동": {"color": "#FFF176", "query_type": "ItemNewAll", "category_id": "13789"},  # 아동
    "자연/여행": {"color": "#A8D5BA", "query_type": "ItemNewAll", "category_id": "1196"},  # 자연/여행
    "SF/공상과학": {"color": "#76FF7A", "query_type": "ItemNewAll", "category_id": "50924"},  # SF 소설
    "경제/경영": {"color": "#256D1B", "query_type": "ItemNewAll", "category_id": "170"},  # 경제/경영
    "건강/의학": {"color": "#C1E1C1", "query_type": "ItemNewAll", "category_id": "51373"}  # 건강/의학
}

def get_books_by_category(category_name, category_info):
    params = {
        "ttbkey": TTB_KEY,
        "QueryType": category_info["query_type"],
        "MaxResults": 5,
        "start": 1,
        "SearchTarget": "Book",
        "output": "js",
        "Version": "20131101",
        "CategoryId": category_info["category_id"]
    }
    
    try:
        response = requests.get(BASE_URL, params=params)
        data = response.json()
        
        if "item" not in data:
            print(f"카테고리 {category_name}에 대한 결과가 없습니다.")
            return []
        
        books = []
        for item in data["item"]:
            book = {
                "title": item.get("title", ""),
                "author": item.get("author", ""),
                "publisher": item.get("publisher", ""),
                "pubDate": item.get("pubDate", ""),
                "description": item.get("description", ""),
                "isbn13": item.get("isbn13", ""),
                "cover": item.get("cover", ""),
                "categoryName": category_name,
                "categoryColor": category_info["color"],
                "price": item.get("priceStandard", 0)
            }
            books.append(book)
        
        return books
    except Exception as e:
        print(f"카테고리 {category_name} 처리 중 오류 발생: {str(e)}")
        return []

# 모든 카테고리에서 책 정보 수집
all_books = []
for category_name, category_info in CATEGORIES.items():
    print(f"{category_name} 카테고리 도서 수집 중...")
    books = get_books_by_category(category_name, category_info)
    all_books.extend(books)
    time.sleep(1)  # API 호출 간 딜레이

# 결과를 JSON 파일로 저장
output_filename = f"books_{datetime.now().strftime('%Y%m%d')}.json"
with open(output_filename, "w", encoding="utf-8") as f:
    json.dump({"books": all_books}, f, ensure_ascii=False, indent=2)

print(f"도서 정보가 {output_filename}에 저장되었습니다.")
print(f"총 {len(all_books)}권의 도서 정보가 수집되었습니다.")
