import asyncio
import gc
import weakref

class TaskMemoryManagement:
    async def demonstrate_task_references(self):
        """Task 객체의 메모리 관리와 참조 추적"""
        
        async def sample_task():
            await asyncio.sleep(0.1)
            return "완료"
        
        # 1. 강한 참조 생성
        tasks = []
        task = asyncio.create_task(sample_task())
        tasks.append(task)  # 리스트가 태스크를 강하게 참조
        
        # 2. 약한 참조로 추적
        weak_ref = weakref.ref(task)
        print(f"약한 참조로 접근: {weak_ref()}")
        
        # 3. Task 완료 대기
        result = await task
        print(f"결과: {result}")
        
        # 4. 참조 해제 테스트
        del task  # 강한 참조 하나 제거
        print(f"task 변수 삭제 후 약한 참조: {weak_ref()}")  # 여전히 존재 (tasks 리스트가 참조)
        
        tasks.clear()  # 모든 강한 참조 제거
        gc.collect()   # 가비지 컬렉션 강제 실행
        print(f"모든 참조 제거 후: {weak_ref()}")  # None
        
        return result

# Task 생성 시 내부적으로 일어나는 일들의 타임라인
class TaskCreationTimeline:
    async def trace_task_creation(self):
        """create_task 호출 시 정확한 실행 순서"""
        
        print("=== Task 생성 과정 추적 ===")
        
        async def traced_coroutine():
            print("  5. 코루틴 내부: 첫 번째 실행")
            await asyncio.sleep(0.1)
            print("  7. 코루틴 내부: sleep 후 재개")
            return "완료"
        
        print("1. 코루틴 객체 생성")
        coro = traced_coroutine()
        
        print("2. create_task 호출")
        task = asyncio.create_task(coro)
        
        print("3. Task 객체 생성 완료")
        print("4. 이벤트 루프 스케줄링 완료")
        
        print("6. 첫 번째 await에서 일시 정지")
        
        return task

# 실제 실행 예제
async def main():
    print("=" * 50)
    print("TASK 메모리 관리 데모")
    print("=" * 50)
    
    # Task 메모리 관리 테스트
    memory_mgmt = TaskMemoryManagement()
    await memory_mgmt.demonstrate_task_references()
    
    print("\n" + "=" * 50)
    print("TASK 생성 과정 추적 데모")
    print("=" * 50)
    
    # Task 생성 과정 추적
    timeline = TaskCreationTimeline()
    task = await timeline.trace_task_creation()
    
    print("\n" + "=" * 50)
    print("기본 TASK 상태 확인 데모")
    print("=" * 50)
    
    # Task 생성과 실행
    task = asyncio.create_task(asyncio.sleep(1))
    
    print(f"Task 생성 직후:")
    print(f"  - done(): {task.done()}")
    print(f"  - cancelled(): {task.cancelled()}")
    print(f"  - _state: {task._state}")
    
    # Task 완료 대기
    await task
    
    print(f"Task 완료 후:")
    print(f"  - done(): {task.done()}")
    print(f"  - result(): {task.result()}")

# 추가 실험: Task의 내부 구조 분석
async def advanced_task_analysis():
    print("\n" + "=" * 50)
    print("고급 TASK 분석")
    print("=" * 50)
    
    async def complex_task(task_id, delay):
        print(f"Task {task_id} 시작 (지연: {delay}초)")
        await asyncio.sleep(delay)
        print(f"Task {task_id} 완료")
        return f"Task {task_id} 결과"
    
    # 여러 태스크 동시 생성 및 관리
    tasks = []
    for i in range(3):
        task = asyncio.create_task(complex_task(i, 0.5 + i * 0.2))
        tasks.append(task)
        print(f"Task {i} 생성됨: {task}")
    
    print(f"\n생성된 태스크 수: {len(tasks)}")
    
    # 모든 태스크 완료 대기
    results = await asyncio.gather(*tasks)
    print(f"모든 결과: {results}")
    
    # 태스크 상태 확인
    for i, task in enumerate(tasks):
        print(f"Task {i} 최종 상태: done={task.done()}, result={task.result()}")

# 실행 함수들
async def run_all_demos():
    """모든 데모를 순차적으로 실행"""
    await main()
    await advanced_task_analysis()

# 메인 실행부
if __name__ == "__main__":
    print("Python asyncio Task 데모 시작...")
    asyncio.run(run_all_demos())
    print("\n데모 완료!")