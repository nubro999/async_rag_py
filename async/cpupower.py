import asyncio
import time
import threading
import psutil
import os

class CPUUtilizationAnalysis:
    
    def measure_cpu_during_sync_io(self):
        """동기식 I/O 중 CPU 사용률 측정"""
        
        def io_heavy_task():
            """I/O 집약적 작업 시뮬레이션"""
            for i in range(5):
                print(f"동기 I/O 작업 {i+1}/5")
                time.sleep(1)  # I/O 대기 시뮬레이션
        
        print("=== 동기식 I/O 중 CPU 모니터링 ===")
        
        # CPU 사용률 모니터링
        cpu_samples = []
        
        def monitor_cpu():
            for _ in range(8):
                cpu_percent = psutil.cpu_percent(interval=0.5)
                cpu_samples.append(cpu_percent)
                print(f"CPU 사용률: {cpu_percent:.1f}%")
        
        # 모니터링 시작
        monitor_thread = threading.Thread(target=monitor_cpu, daemon=True)
        monitor_thread.start()
        
        # I/O 작업 실행
        start = time.time()
        io_heavy_task()
        end = time.time()
        
        monitor_thread.join()
        
        avg_cpu = sum(cpu_samples) / len(cpu_samples) if cpu_samples else 0
        
        print(f"동기식 실행 시간: {end - start:.1f}초")
        print(f"평균 CPU 사용률: {avg_cpu:.1f}%")
        print("분석: I/O 대기로 인한 낮은 CPU 활용도")
        
        return end - start, avg_cpu
    
    async def measure_cpu_during_async_io(self):
        """비동기식 I/O 중 CPU 사용률 측정"""
        
        async def async_io_task(task_id):
            """비동기 I/O 작업"""
            for i in range(5):
                print(f"비동기 I/O 작업 {task_id}-{i+1}/5")
                await asyncio.sleep(1)  # 다른 태스크에게 제어권 양보
        
        print("\n=== 비동기식 I/O 중 CPU 모니터링 ===")
        
        # CPU 모니터링 코루틴
        cpu_samples = []
        
        async def monitor_cpu_async():
            for _ in range(8):
                await asyncio.sleep(0.5)
                cpu_percent = psutil.cpu_percent()
                cpu_samples.append(cpu_percent)
                print(f"CPU 사용률: {cpu_percent:.1f}%")
        
        # 여러 I/O 작업을 동시에 실행
        start = time.time()
        
        await asyncio.gather(
            async_io_task("A"),
            async_io_task("B"), 
            async_io_task("C"),
            monitor_cpu_async()
        )
        
        end = time.time()
        
        avg_cpu = sum(cpu_samples) / len(cpu_samples) if cpu_samples else 0
        
        print(f"비동기식 실행 시간: {end - start:.1f}초")
        print(f"평균 CPU 사용률: {avg_cpu:.1f}%")
        print("분석: 더 효율적인 CPU 활용 (여러 작업 동시 처리)")
        
        return end - start, avg_cpu

# 간단한 I/O vs CPU 비교 데모
class SimpleComparison:
    
    def sync_multiple_operations(self):
        """동기식 다중 작업"""
        print("=== 동기식 다중 작업 ===")
        
        def single_operation(op_id):
            print(f"작업 {op_id} 시작")
            time.sleep(1)  # I/O 시뮬레이션
            print(f"작업 {op_id} 완료")
            return f"결과 {op_id}"
        
        start = time.time()
        results = []
        
        # 순차적으로 실행
        for i in range(3):
            result = single_operation(i)
            results.append(result)
        
        end = time.time()
        
        print(f"동기식 총 시간: {end - start:.1f}초")
        print(f"결과: {results}")
        
        return end - start
    
    async def async_multiple_operations(self):
        """비동기식 다중 작업"""
        print("\n=== 비동기식 다중 작업 ===")
        
        async def single_operation(op_id):
            print(f"작업 {op_id} 시작")
            await asyncio.sleep(1)  # I/O 시뮬레이션
            print(f"작업 {op_id} 완료")
            return f"결과 {op_id}"
        
        start = time.time()
        
        # 동시에 실행
        tasks = [single_operation(i) for i in range(3)]
        results = await asyncio.gather(*tasks)
        
        end = time.time()
        
        print(f"비동기식 총 시간: {end - start:.1f}초")
        print(f"결과: {results}")
        
        return end - start

# CPU vs I/O 바운드 작업 비교
class WorkloadComparison:
    
    def cpu_bound_demo(self):
        """CPU 집약적 작업 - async 이점 없음"""
        print("\n=== CPU 집약적 작업 (async 이점 없음) ===")
        
        def calculate_squares(n):
            total = 0
            for i in range(n):
                total += i * i
            return total
        
        # 동기식 CPU 작업
        start = time.time()
        result1 = calculate_squares(1000000)
        result2 = calculate_squares(1000000)
        result3 = calculate_squares(1000000)
        sync_time = time.time() - start
        
        print(f"동기식 CPU 작업 시간: {sync_time:.2f}초")
        print(f"결과들: {result1}, {result2}, {result3}")
        print("CPU가 계속 바쁘므로 async의 이점이 없음")
        
        return sync_time
    
    async def io_bound_demo(self):
        """I/O 집약적 작업 - async 이점 큼"""
        print("\n=== I/O 집약적 작업 (async 이점 큼) ===")
        
        async def fetch_data(source_id):
            print(f"데이터 소스 {source_id}에서 가져오는 중...")
            await asyncio.sleep(1)  # 네트워크/DB 지연 시뮬레이션
            return f"데이터 from {source_id}"
        
        start = time.time()
        
        # 여러 소스에서 동시에 데이터 가져오기
        tasks = [fetch_data(i) for i in range(3)]
        results = await asyncio.gather(*tasks)
        
        async_time = time.time() - start
        
        print(f"비동기식 I/O 작업 시간: {async_time:.2f}초")
        print(f"결과들: {results}")
        print("I/O 대기 중 다른 작업 처리로 빠른 완료")
        
        return async_time

# 메인 실행 함수들
async def run_cpu_analysis():
    """CPU 사용률 분석 실행"""
    analyzer = CPUUtilizationAnalysis()
    
    # 동기식 분석
    sync_time, sync_cpu = analyzer.measure_cpu_during_sync_io()
    
    # 비동기식 분석
    async_time, async_cpu = await analyzer.measure_cpu_during_async_io()
    
    print(f"\n=== CPU 분석 결과 ===")
    print(f"동기식: {sync_time:.1f}초, CPU: {sync_cpu:.1f}%")
    print(f"비동기식: {async_time:.1f}초, CPU: {async_cpu:.1f}%")

async def run_simple_comparison():
    """간단한 성능 비교"""
    comparison = SimpleComparison()
    
    sync_time = comparison.sync_multiple_operations()
    async_time = await comparison.async_multiple_operations()
    
    print(f"\n=== 성능 비교 결과 ===")
    print(f"동기식: {sync_time:.1f}초")
    print(f"비동기식: {async_time:.1f}초")
    print(f"성능 향상: {sync_time / async_time:.1f}배 빠름")

async def run_workload_comparison():
    """작업 유형별 비교"""
    workload = WorkloadComparison()
    
    cpu_time = workload.cpu_bound_demo()
    io_time = await workload.io_bound_demo()
    
    print(f"\n=== 작업 유형별 비교 ===")
    print(f"CPU 집약적 작업: {cpu_time:.2f}초")
    print(f"I/O 집약적 작업: {io_time:.2f}초")
    print("결론: I/O 작업에서만 async가 효과적")

# 전체 데모 실행
async def main():
    """모든 데모를 순차적으로 실행"""
    print("Python 비동기 성능 분석 시작...\n")
    
    try:
        await run_simple_comparison()
        print("\n" + "="*60)
        
        await run_workload_comparison()
        print("\n" + "="*60)
        
        # CPU 분석은 psutil이 필요하므로 선택적 실행
        try:
            await run_cpu_analysis()
        except ImportError:
            print("psutil이 설치되지 않아 CPU 분석을 건너뜁니다.")
            print("설치: pip install psutil")
        
    except Exception as e:
        print(f"실행 중 오류 발생: {e}")
    
    print("\n분석 완료!")

# 실행부
if __name__ == "__main__":
    print("비동기 성능 분석 데모")
    print("=" * 50)
    asyncio.run(main())