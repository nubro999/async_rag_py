# RAG 시스템 빠른 시작 가이드

## 5분 안에 시작하기

### 1단계: 패키지 설치 (2분)

```bash
cd rag
pip install -r requirements.txt
```

### 2단계: API 키 설정 (1분)

**Windows PowerShell:**
```powershell
$env:OPENAI_API_KEY="your-api-key-here"
```

**Linux/Mac:**
```bash
export OPENAI_API_KEY='your-api-key-here'
```

### 3단계: 실행 (2분)

**기본 RAG 실행:**
```bash
python rag.py
```

**스마트 RAG 실행:**
```bash
python rag_smart.py
```

## 문서 구조 한눈에 보기

```
rag/
├── 📄 rag.py              ← 기본 RAG (여기서 시작!)
├── 🧠 rag_smart.py        ← 스마트 RAG (다중 문서용)
├── 📦 requirements.txt    ← 필수 패키지 목록
│
├── 📚 docs/               ← 스마트 RAG 문서 저장소
│   ├── ⚙️ doc_metadata.json
│   ├── 📊 trading/
│   ├── 🛡️ risk/
│   ├── 📈 technical/
│   └── 📋 general/
│
└── 📖 README.md           ← 전체 문서
```

## 빠른 테스트

### 테스트 1: 기본 RAG
```bash
python rag.py
```
**예상 출력:**
```
📄 문서 로딩 중...
✅ 1개 문서 로드 완료
✂️ 텍스트 청크 분할 중...
✅ 1개 청크로 분할 완료
...
```

### 테스트 2: 스마트 RAG
```bash
python rag_smart.py
```
**예상 출력:**
```
🎯 선택된 카테고리: trading
📄 선택된 문서 로딩...
✅ 로드: strategies.txt
...
```

## 자주 묻는 질문

### Q: ImportError가 발생해요
**A:** 패키지 재설치
```bash
pip install --upgrade langchain langchain-community langchain-openai langchain-chroma chromadb openai
```

### Q: API 키 오류가 나요
**A:** API 키 확인
```bash
# Windows
echo $env:OPENAI_API_KEY

# Linux/Mac
echo $OPENAI_API_KEY
```

### Q: 답변이 이상해요
**A:**
1. 문서 내용 확인 (company_docs.txt 또는 docs/ 폴더)
2. 질문을 더 구체적으로 변경
3. 관련 키워드가 메타데이터에 있는지 확인

### Q: 느려요
**A:**
- 기본 RAG: chunk_size를 500으로 줄이기
- 스마트 RAG: 이미 최적화되어 있음, 문서 개수 확인

## 다음 단계

✅ 기본 RAG 실행 완료
→ ✅ 스마트 RAG 실행 완료
  → ✅ 자신의 문서 추가
    → ✅ 메타데이터 커스터마이징
      → 🚀 프로덕션 배포!

## 추가 자료

- [README.md](README.md) - 전체 문서
- [COMPARISON.md](COMPARISON.md) - 두 시스템 비교
- [LangChain 문서](https://python.langchain.com/)

## 문제 발생 시

1. requirements.txt 재확인
2. Python 버전 확인 (3.8 이상)
3. API 크레딧 확인
4. 네트워크 연결 확인

여전히 문제가 있다면 README.md의 "문제 해결" 섹션 참조!
