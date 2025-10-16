import os
from pathlib import Path

try:
    from langchain_community.document_loaders import TextLoader
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain_openai import OpenAIEmbeddings, ChatOpenAI
    from langchain_chroma import Chroma
    from langchain.chains import RetrievalQA
except ImportError as e:
    raise ImportError(f"Missing required package: {e}")


def setup_environment():
    """환경 설정 및 검증"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY 환경 변수가 설정되지 않았습니다.\n"
            "설정 방법: export OPENAI_API_KEY='your-api-key'"
        )
    return api_key


def ensure_data_file(file_path: str) -> Path:
    """데이터 파일 존재 확인 및 생성"""
    path = Path(file_path)
    if not path.exists():
        print(f"{file_path} 파일이 없어 샘플 데이터를 생성합니다...")
        sample_content = """
트레이딩 전략

1. 시장 분석 기반 전략
- 기술적 분석과 기본적 분석을 결합하여 시장 동향 파악
- 다양한 지표(RSI, MACD, 볼린저 밴드 등)를 활용한 진입/청산 시점 결정

2. 리스크 관리
- 포지션 크기는 포트폴리오의 2% 이하로 제한
- 손절매 라인 설정 필수
- 다양한 자산군에 분산 투자

3. 자동화 시스템
- AI 기반 신호 감지 시스템 운영
- 24/7 시장 모니터링
- 백테스팅을 통한 전략 검증

4. 성과 분석
- 일일/주간/월간 성과 리포트 생성
- 샤프 비율, 최대 낙폭 등 주요 지표 추적
- 지속적인 전략 개선 및 최적화
"""
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(sample_content, encoding='utf-8')
        print(f"✅ {file_path} 파일을 생성했습니다.")
    return path


def create_rag_system(doc_path: str, persist_dir: str = "./chroma_db"):
    """RAG 시스템 생성"""

    # 1. 문서 로드
    print("문서 로딩 중...")
    loader = TextLoader(str(doc_path), encoding='utf-8')
    documents = loader.load()
    print(f"✅ {len(documents)}개 문서 로드 완료")

    # 2. 청크 분할
    print("텍스트 청크 분할 중...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    texts = text_splitter.split_documents(documents)
    print(f"{len(texts)}개 청크로 분할 완료")

    # 3. 벡터 DB 생성
    print("임베딩 및 벡터 DB 생성 중...")
    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma.from_documents(
        documents=texts,
        embedding=embeddings,
        persist_directory=persist_dir
    )
    print("벡터 DB 생성 완료")

    # 4. RAG 체인 생성
    print("RAG 체인 구성 중...")
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(
            search_kwargs={"k": 3}
        ),
        return_source_documents=True,
    )
    print("RAG 시스템 준비 완료\n")

    return qa_chain


def ask_question(qa_chain, question: str):
    """질문 처리 및 결과 출력"""
    print(f"질문: {question}")
    print("생각 중...\n")

    result = qa_chain.invoke({"query": question})

    print("답변:")
    print("-" * 50)
    print(result["result"])
    print("-" * 50)

    if "source_documents" in result:
        print(f"\n참조 문서: {len(result['source_documents'])}개")

    return result


def main():
    """메인 실행 함수"""
    try:
        # 환경 설정
        setup_environment()

        # 데이터 파일 확인
        doc_path = ensure_data_file("company_docs.txt")

        # RAG 시스템 생성
        qa_chain = create_rag_system(str(doc_path))

        # 질문 예시
        questions = [
            "회사의 트레이딩 전략은?",
            "리스크 관리 방법은?",
            "자동화 시스템의 특징은?"
        ]

        for i, question in enumerate(questions, 1):
            print(f"\n{'='*60}")
            print(f"질문 {i}/{len(questions)}")
            print(f"{'='*60}\n")
            ask_question(qa_chain, question)

        print("\n✅ RAG 데모 완료!")

    except ValueError as e:
        print(f"❌ 설정 오류: {e}")
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        raise


if __name__ == "__main__":
    main()