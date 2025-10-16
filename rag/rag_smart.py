"""
스마트 RAG 시스템 - AI가 질문에 따라 적절한 문서를 자동 선택

필수 패키지 설치:
pip install langchain langchain-community langchain-openai langchain-chroma chromadb openai
"""
import os
import json
from pathlib import Path
from typing import List, Dict, Set

try:
    from langchain_community.document_loaders import TextLoader, DirectoryLoader
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain_openai import OpenAIEmbeddings, ChatOpenAI
    from langchain_chroma import Chroma
    from langchain.chains import RetrievalQA
    from langchain.schema import Document
except ImportError as e:
    print(f"❌ 필수 패키지 설치 필요:")
    print(f"   pip install langchain langchain-community langchain-openai langchain-chroma chromadb openai")
    raise ImportError(f"Missing required package: {e}")


class SmartDocumentSelector:
    """질문 분석 후 적절한 문서 카테고리 선택"""

    def __init__(self, metadata_path: str = "docs/doc_metadata.json"):
        self.metadata_path = Path(metadata_path)
        self.metadata = self._load_metadata()

    def _load_metadata(self) -> Dict:
        """메타데이터 로드"""
        if not self.metadata_path.exists():
            print(f"⚠️  메타데이터 파일이 없습니다: {self.metadata_path}")
            return {"categories": {}, "default_category": "general"}

        with open(self.metadata_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def analyze_query(self, query: str) -> List[str]:
        """
        질문을 분석하여 관련 카테고리 반환

        Returns:
            카테고리 이름 리스트 (관련도 순)
        """
        query_lower = query.lower()
        category_scores = {}

        for category, info in self.metadata['categories'].items():
            score = 0
            keywords = info['keywords']

            # 키워드 매칭
            for keyword in keywords:
                if keyword.lower() in query_lower:
                    score += 1

            if score > 0:
                category_scores[category] = score

        # 점수 순으로 정렬
        if category_scores:
            sorted_categories = sorted(
                category_scores.items(),
                key=lambda x: x[1],
                reverse=True
            )
            selected = [cat for cat, score in sorted_categories]
            print(f"🎯 선택된 카테고리: {', '.join(selected)}")
            return selected
        else:
            default = self.metadata.get('default_category', 'general')
            print(f"🎯 기본 카테고리 사용: {default}")
            return [default]

    def get_document_paths(self, categories: List[str], base_path: str = "docs") -> List[str]:
        """카테고리에 해당하는 문서 경로 반환"""
        paths = []
        base = Path(base_path)

        for category in categories:
            if category in self.metadata['categories']:
                files = self.metadata['categories'][category]['files']
                for file in files:
                    full_path = base / file
                    if full_path.exists():
                        paths.append(str(full_path))
                    else:
                        print(f"⚠️  파일 없음: {full_path}")

        return paths


class SmartRAGSystem:
    """스마트 RAG 시스템"""

    def __init__(self, docs_base_path: str = "docs"):
        self.docs_base_path = Path(docs_base_path)
        self.selector = SmartDocumentSelector()
        self.embeddings = OpenAIEmbeddings()
        self.llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )

    def load_documents(self, file_paths: List[str]) -> List[Document]:
        """지정된 파일들에서 문서 로드"""
        documents = []

        for file_path in file_paths:
            try:
                loader = TextLoader(file_path, encoding='utf-8')
                docs = loader.load()
                documents.extend(docs)
                print(f"✅ 로드: {Path(file_path).name}")
            except Exception as e:
                print(f"❌ 로드 실패: {file_path} - {e}")

        return documents

    def load_all_documents(self) -> List[Document]:
        """모든 문서 로드 (초기 벡터 DB 생성용)"""
        print(f"📚 모든 문서 로딩: {self.docs_base_path}")

        documents = []
        for txt_file in self.docs_base_path.rglob("*.txt"):
            try:
                loader = TextLoader(str(txt_file), encoding='utf-8')
                docs = loader.load()
                documents.extend(docs)
                print(f"✅ {txt_file.relative_to(self.docs_base_path)}")
            except Exception as e:
                print(f"❌ {txt_file.name}: {e}")

        return documents

    def create_vectorstore(self, documents: List[Document], persist_dir: str = "./chroma_db") -> Chroma:
        """벡터 DB 생성"""
        print(f"✂️  {len(documents)}개 문서를 청크로 분할 중...")
        texts = self.text_splitter.split_documents(documents)
        print(f"✅ {len(texts)}개 청크 생성 완료")

        print("🔢 벡터 DB 생성 중...")
        vectorstore = Chroma.from_documents(
            documents=texts,
            embedding=self.embeddings,
            persist_directory=persist_dir
        )
        print("✅ 벡터 DB 생성 완료")

        return vectorstore

    def create_qa_chain(self, vectorstore: Chroma, k: int = 3) -> RetrievalQA:
        """QA 체인 생성"""
        qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=vectorstore.as_retriever(search_kwargs={"k": k}),
            return_source_documents=True,
        )
        return qa_chain

    def ask_with_smart_selection(self, query: str, use_all: bool = False) -> Dict:
        """
        스마트 문서 선택 후 질문 처리

        Args:
            query: 질문
            use_all: True면 모든 문서 사용, False면 관련 문서만 선택
        """
        print(f"\n❓ 질문: {query}")
        print("="*60)

        if use_all:
            print("📚 모든 문서 사용 모드")
            documents = self.load_all_documents()
        else:
            print("🎯 스마트 문서 선택 모드")
            # 질문 분석
            categories = self.selector.analyze_query(query)

            # 관련 문서 경로 가져오기
            file_paths = self.selector.get_document_paths(categories, str(self.docs_base_path))

            if not file_paths:
                print("⚠️  관련 문서를 찾지 못했습니다. 모든 문서를 사용합니다.")
                documents = self.load_all_documents()
            else:
                print(f"📄 선택된 문서 로딩...")
                documents = self.load_documents(file_paths)

        if not documents:
            return {"error": "로드된 문서가 없습니다."}

        # 벡터 DB 생성 (임시)
        vectorstore = self.create_vectorstore(documents, persist_dir="./temp_chroma_db")

        # QA 체인 생성 및 질문
        qa_chain = self.create_qa_chain(vectorstore)

        print("💭 생각 중...\n")
        result = qa_chain.invoke({"query": query})

        # 결과 출력
        print("📝 답변:")
        print("-" * 60)
        print(result["result"])
        print("-" * 60)

        if "source_documents" in result:
            print(f"\n📚 참조 문서: {len(result['source_documents'])}개")
            # 참조된 고유 파일 표시
            sources = set()
            for doc in result['source_documents']:
                if 'source' in doc.metadata:
                    sources.add(Path(doc.metadata['source']).name)
            if sources:
                print(f"   파일: {', '.join(sources)}")

        return result


def setup_environment():
    """환경 설정 및 검증"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY 환경 변수가 설정되지 않았습니다.\n"
            "설정 방법: export OPENAI_API_KEY='your-api-key'"
        )
    return api_key


def main():
    """메인 실행 함수"""
    try:
        print("🚀 스마트 RAG 시스템 시작\n")

        # 환경 설정
        setup_environment()

        # RAG 시스템 초기화
        rag = SmartRAGSystem(docs_base_path="docs")

        # 테스트 질문들
        questions = [
            ("회사의 트레이딩 전략에는 어떤 것들이 있나요?", False),
            ("RSI 지표는 어떻게 사용하나요?", False),
            ("리스크 관리에서 손절매는 어떻게 설정하나요?", False),
            ("회사의 비전은 무엇인가요?", False),
            ("볼린저 밴드와 포지션 사이징을 함께 설명해주세요", True),  # 여러 카테고리
        ]

        for i, (question, use_all) in enumerate(questions, 1):
            print(f"\n{'='*60}")
            print(f"질문 {i}/{len(questions)}")
            print(f"{'='*60}")

            result = rag.ask_with_smart_selection(question, use_all=use_all)

            if "error" not in result:
                print(f"\n✅ 질문 {i} 완료")
            else:
                print(f"\n❌ 질문 {i} 오류: {result['error']}")

        print("\n" + "="*60)
        print("✅ 스마트 RAG 데모 완료!")
        print("="*60)

    except ValueError as e:
        print(f"❌ 설정 오류: {e}")
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        raise


if __name__ == "__main__":
    main()
