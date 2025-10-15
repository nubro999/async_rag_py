import asyncio
import time
from typing import List
import aiohttp
from datetime import datetime


# 예제 1: 기본 async/await
async def example1_basic_async():
    print("\n=== 예제 1: 기본 async/await ===")
    
    # 동기 방식
    print("동기 실행 시작...")
    start = time.time()
    time.sleep(1)
    print(f"동기 실행 완료 ({time.time() - start:.2f}초)")
    
    # 비동기 방식
    print("\n비동기 실행 시작...")
    start = time.time()
    await asyncio.sleep(1)
    print(f"비동기 실행 완료 ({time.time() - start:.2f}초)")


# 예제 2: 여러 작업 동시 실행
async def fetch_data(name: str, delay: int):
    print(f"{name} 시작...")
    await asyncio.sleep(delay)
    print(f"{name} 완료!")
    return f"{name} 결과"


async def example2_gather():
    print("\n=== 예제 2: asyncio.gather (동시 실행) ===")
    
    start = time.time()
    
    # 순차 실행 (비교용)
    # await fetch_data("Task 1", 2)
    # await fetch_data("Task 2", 1)
    # await fetch_data("Task 3", 1)
    # 총 4초 소요
    
    # 동시 실행
    results = await asyncio.gather(
        fetch_data("Task 1", 2),
        fetch_data("Task 2", 1),
        fetch_data("Task 3", 1)
    )
    
    elapsed = time.time() - start
    print(f"\n결과: {results}")
    print(f"총 소요 시간: {elapsed:.2f}초 (동시 실행으로 단축!)")


# 예제 3: Task 생성과 관리
async def example3_tasks():
    print("\n=== 예제 3: Task 생성과 관리 ===")
    
    # Task 생성
    task1 = asyncio.create_task(fetch_data("Background Task 1", 2))
    task2 = asyncio.create_task(fetch_data("Background Task 2", 1))
    
    print("Task들이 백그라운드에서 실행 중...")
    await asyncio.sleep(0.5)
    print("메인 코드는 계속 실행됨")
    
    # Task 완료 대기
    result1 = await task1
    result2 = await task2
    
    print(f"최종 결과: {result1}, {result2}")


# 예제 4: asyncio.wait와 타임아웃
async def slow_task(name: str, delay: int):
    await asyncio.sleep(delay)
    return f"{name} (지연: {delay}초)"


async def example4_wait_timeout():
    print("\n=== 예제 4: asyncio.wait와 타임아웃 ===")
    
    tasks = [
        asyncio.create_task(slow_task("빠른 작업", 1)),
        asyncio.create_task(slow_task("보통 작업", 2)),
        asyncio.create_task(slow_task("느린 작업", 3))
    ]
    
    # 2초 타임아웃으로 완료된 작업만 가져오기
    done, pending = await asyncio.wait(tasks, timeout=2)
    
    print(f"완료된 작업: {len(done)}개")
    for task in done:
        print(f"  - {task.result()}")
    
    print(f"미완료 작업: {len(pending)}개")
    
    # 남은 작업 취소
    for task in pending:
        task.cancel()
    
    print("미완료 작업 취소됨")


# 예제 5: 비동기 제너레이터 (스트리밍)
async def stream_data(count: int):
    for i in range(1, count + 1):
        await asyncio.sleep(0.5)
        yield f"데이터 청크 {i}"


async def example5_async_generator():
    print("\n=== 예제 5: 비동기 제너레이터 ===")
    
    async for data in stream_data(5):
        print(f"수신: {data}")


# 예제 6: 세마포어로 동시 실행 제한
async def limited_task(sem: asyncio.Semaphore, task_id: int):
    async with sem:  # 동시 실행 수 제한
        print(f"Task {task_id} 시작")
        await asyncio.sleep(1)
        print(f"Task {task_id} 완료")
        return task_id


async def example6_semaphore():
    print("\n=== 예제 6: 세마포어 (동시 실행 제한) ===")
    
    # 최대 2개만 동시 실행
    sem = asyncio.Semaphore(2)
    
    tasks = [limited_task(sem, i) for i in range(5)]
    results = await asyncio.gather(*tasks)
    
    print(f"모든 작업 완료: {results}")


# 예제 7: 블록체인 트랜잭션 처리 시뮬레이션
class Transaction:
    def __init__(self, tx_id: int, from_addr: str, to_addr: str, amount: float):
        self.id = tx_id
        self.from_addr = from_addr
        self.to_addr = to_addr
        self.amount = amount


async def validate_transaction(tx: Transaction) -> str:
    """트랜잭션 검증 시뮬레이션"""
    print(f"TX #{tx.id} 검증 중... ({tx.from_addr} -> {tx.to_addr}, {tx.amount} ETH)")
    await asyncio.sleep(1)  # 네트워크 검증 시뮬레이션
    return f"TX #{tx.id} 검증 완료"


async def broadcast_transaction(tx: Transaction) -> str:
    """트랜잭션 브로드캐스트 시뮬레이션"""
    print(f"TX #{tx.id} 브로드캐스트 중...")
    await asyncio.sleep(0.5)
    return f"TX #{tx.id} 브로드캐스트 완료"


async def process_transaction(tx: Transaction):
    """트랜잭션 전체 처리"""
    validation = await validate_transaction(tx)
    broadcast = await broadcast_transaction(tx)
    return f"{validation}, {broadcast}"


async def example7_blockchain_simulation():
    print("\n=== 예제 7: 블록체인 트랜잭션 처리 ===")
    
    transactions = [
        Transaction(1, "0xABC", "0xDEF", 1.5),
        Transaction(2, "0x123", "0x456", 2.0),
        Transaction(3, "0x789", "0xAAA", 0.5),
    ]
    
    start = time.time()
    
    # 모든 트랜잭션 동시 처리
    results = await asyncio.gather(*[process_transaction(tx) for tx in transactions])
    
    elapsed = time.time() - start
    
    print("\n처리 결과:")
    for result in results:
        print(f"  ✓ {result}")
    print(f"총 소요 시간: {elapsed:.2f}초")


# 예제 8: 비동기 컨텍스트 매니저
class AsyncResource:
    async def __aenter__(self):
        print("리소스 연결 중...")
        await asyncio.sleep(0.5)
        print("리소스 연결 완료")
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print("리소스 정리 중...")
        await asyncio.sleep(0.5)
        print("리소스 정리 완료")
    
    async def fetch(self):
        await asyncio.sleep(0.5)
        return "데이터"


async def example8_async_context_manager():
    print("\n=== 예제 8: 비동기 컨텍스트 매니저 ===")
    
    async with AsyncResource() as resource:
        data = await resource.fetch()
        print(f"가져온 데이터: {data}")


# 예제 9: 비동기 HTTP 요청 (aiohttp 필요)
async def example9_async_http():
    print("\n=== 예제 9: 비동기 HTTP 요청 ===")
    print("(실제 실행하려면 'pip install aiohttp' 필요)")
    
    # aiohttp 사용 예제 코드 (주석 처리)
    """
    urls = [
        'https://jsonplaceholder.typicode.com/posts/1',
        'https://jsonplaceholder.typicode.com/posts/2',
        'https://jsonplaceholder.typicode.com/posts/3',
    ]
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            tasks.append(session.get(url))
        
        responses = await asyncio.gather(*tasks)
        
        for i, response in enumerate(responses):
            data = await response.json()
            print(f"응답 {i+1}: {data['title']}")
    """
    
    print("위 코드의 시뮬레이션:")
    await asyncio.gather(
        fetch_data("API 요청 1", 1),
        fetch_data("API 요청 2", 1),
        fetch_data("API 요청 3", 1)
    )


# 예제 10: 에러 처리
async def failing_task(task_id: int):
    await asyncio.sleep(1)
    if task_id == 2:
        raise ValueError(f"Task {task_id} 실패!")
    return f"Task {task_id} 성공"


async def example10_error_handling():
    print("\n=== 예제 10: 에러 처리 ===")
    
    tasks = [failing_task(i) for i in range(1, 4)]
    
    # return_exceptions=True로 예외를 결과로 받음
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            print(f"Task {i+1}: 에러 발생 - {result}")
        else:
            print(f"Task {i+1}: {result}")


# 메인 실행 함수
async def main():
    print("=" * 50)
    print("Python 비동기 처리 예제 모음")
    print("=" * 50)
    
    await example1_basic_async()
    await example2_gather()
    await example3_tasks()
    await example4_wait_timeout()
    await example5_async_generator()
    await example6_semaphore()
    await example7_blockchain_simulation()
    await example8_async_context_manager()
    await example9_async_http()
    await example10_error_handling()
    
    print("\n" + "=" * 50)
    print("모든 예제 완료!")
    print("=" * 50)


if __name__ == "__main__":
    # Python 3.7+
    asyncio.run(main())