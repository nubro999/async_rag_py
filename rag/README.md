# RAG (Retrieval-Augmented Generation) 데모

LangChain을 사용한 RAG 시스템 구현 예제

## 버전

1. **rag.py** - 기본 RAG 시스템 (단일 문서)
2. **rag_smart.py** - 스마트 RAG 시스템 (AI가 질문에 따라 적절한 문서 자동 선택)

## 기능

### 기본 기능 (rag.py)
- 문서 로딩 및 청크 분할
- OpenAI 임베딩을 사용한 벡터 DB 생성
- ChromaDB를 활용한 벡터 저장소
- 질의응답 체인 구성
- 자동 샘플 데이터 생성

### 스마트 기능 (rag_smart.py)
- 질문 분석을 통한 자동 카테고리 선택
- 키워드 기반 문서 필터링
- 다중 문서 소스 지원
- 메타데이터 기반 문서 관리
- 카테고리별 문서 조직화

## 설치

### 1. 필수 패키지 설치

```bash
pip install -r requirements.txt
```

또는 개별 설치:

```bash
pip install langchain langchain-community langchain-openai langchain-chroma chromadb openai
```

### 2. 환경 변수 설정

OpenAI API 키 설정:

**Windows (PowerShell):**
```powershell
$env:OPENAI_API_KEY="your-api-key-here"
```

**Windows (CMD):**
```cmd
set OPENAI_API_KEY=your-api-key-here
```

**Linux/Mac:**
```bash
export OPENAI_API_KEY='your-api-key-here'
```

또는 `.env` 파일 생성:

```
OPENAI_API_KEY=your-api-key-here
```

## 사용법

### 기본 RAG 실행

```bash
python rag.py
```

### 스마트 RAG 실행

```bash
python rag_smart.py
```

### 동작 과정

1. **환경 설정 검증** - OPENAI_API_KEY 확인
2. **문서 준비** - `company_docs.txt` 파일 자동 생성 (없는 경우)
3. **문서 로딩** - 텍스트 파일 로드
4. **청크 분할** - 1000자 단위로 분할 (200자 오버랩)
5. **벡터 DB 생성** - OpenAI 임베딩 + ChromaDB
6. **질의응답** - 3개의 예시 질문 처리

## 프로젝트 구조

```
rag/
├── rag.py                    # 기본 RAG 시스템
├── rag_smart.py              # 스마트 RAG 시스템
├── requirements.txt          # 의존성 패키지 목록
├── README.md                 # 이 파일
├── company_docs.txt          # 샘플 문서 (rag.py용)
├── docs/                     # 문서 저장소
│   ├── doc_metadata.json     # 문서 메타데이터 (카테고리, 키워드)
│   ├── trading/              # 트레이딩 전략 문서
│   │   └── strategies.txt
│   ├── risk/                 # 리스크 관리 문서
│   │   └── risk_management.txt
│   ├── technical/            # 기술적 지표 문서
│   │   └── indicators.txt
│   └── general/              # 일반 정보 문서
│       └── company_overview.txt
├── chroma_db/                # 벡터 DB 저장소 (자동 생성)
└── temp_chroma_db/           # 임시 벡터 DB (스마트 RAG용)
```

## 주요 기능 설명

### 기본 RAG (rag.py)

#### setup_environment()
- OpenAI API 키 검증
- 환경 변수 확인

#### ensure_data_file()
- 데이터 파일 존재 확인
- 없으면 샘플 데이터 자동 생성

#### create_rag_system()
- 문서 로드 및 청크 분할
- 임베딩 생성 및 벡터 DB 구축
- RAG 체인 생성

#### ask_question()
- 질문 처리
- 답변 생성 및 출력
- 참조 문서 정보 표시

### 스마트 RAG (rag_smart.py)

#### SmartDocumentSelector
질문 분석 및 문서 선택 엔진
- **analyze_query()**: 질문에서 키워드 추출 및 카테고리 매칭
- **get_document_paths()**: 선택된 카테고리의 문서 경로 반환

예시:
- "RSI 지표는?" → `technical` 카테고리 → `indicators.txt`
- "손절매 설정" → `risk` 카테고리 → `risk_management.txt`
- "회사 비전" → `general` 카테고리 → `company_overview.txt`

#### SmartRAGSystem
통합 RAG 시스템
- **load_documents()**: 선택된 문서만 로드 (효율성)
- **load_all_documents()**: 모든 문서 로드 (포괄성)
- **ask_with_smart_selection()**: 질문 분석 → 문서 선택 → 답변 생성

## 예시 출력

```
📄 문서 로딩 중...
✅ 1개 문서 로드 완료
✂️  텍스트 청크 분할 중...
✅ 1개 청크로 분할 완료
🔢 임베딩 및 벡터 DB 생성 중...
✅ 벡터 DB 생성 완료
🔗 RAG 체인 구성 중...
✅ RAG 시스템 준비 완료

============================================================
질문 1/3
============================================================

❓ 질문: 회사의 트레이딩 전략은?
💭 생각 중...

📝 답변:
--------------------------------------------------
[AI 생성 답변이 여기에 표시됩니다]
--------------------------------------------------

📚 참조 문서: 3개
```

## 커스터마이징

### 새로운 문서 카테고리 추가 (스마트 RAG)

1. **docs/ 폴더에 새 카테고리 디렉토리 생성**
```bash
mkdir docs/new_category
```

2. **해당 카테고리에 문서 추가**
```bash
# docs/new_category/my_document.txt 파일 생성
```

3. **doc_metadata.json 업데이트**
```json
{
  "categories": {
    "new_category": {
      "keywords": ["키워드1", "keyword1", "키워드2"],
      "description": "카테고리 설명",
      "files": ["new_category/my_document.txt"]
    }
  }
}
```

### 기본 RAG 문서 변경

`company_docs.txt` 파일을 직접 생성하거나 수정:

```python
# rag.py에서 파일 경로 변경
doc_path = ensure_data_file("your_custom_file.txt")
```

### 질문 변경

```python
questions = [
    "원하는 질문 1",
    "원하는 질문 2",
    "원하는 질문 3"
]
```

### 청크 크기 조정

```python
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,      # 청크 크기 변경
    chunk_overlap=100,   # 오버랩 크기 변경
)
```

### 검색 결과 개수 조정

```python
retriever=vectorstore.as_retriever(
    search_kwargs={"k": 5}  # 검색 결과 개수 변경
)
```

## 문제 해결

### ImportError 발생 시

```bash
pip install --upgrade langchain langchain-community langchain-openai langchain-chroma
```

### OpenAI API 오류

- API 키가 올바르게 설정되었는지 확인
- API 크레딧이 충분한지 확인
- 네트워크 연결 확인

### ChromaDB 오류

```bash
pip install --upgrade chromadb
```

## 참고 자료

- [LangChain 공식 문서](https://python.langchain.com/)
- [OpenAI API 문서](https://platform.openai.com/docs/)
- [ChromaDB 문서](https://docs.trychroma.com/)

## 라이선스

MIT License
