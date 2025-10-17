import asyncio

class AsyncBestPractices:
    
    async def common_mistakes(self):
        """흔한 실수들과 올바른 방법"""
        
        # ❌ 잘못된 방법: 동기 함수에서 비동기 함수 호출
        def wrong_way():
            # asyncio.sleep(1)  # 오류 발생!
            pass
        
        # ✅ 올바른 방법
        async def correct_way():
            await asyncio.sleep(1)
        
        # ❌ 잘못된 방법: CPU 집약적 작업에 async 사용
        async def wrong_cpu_intensive():
            # CPU 바운드 작업은 async의 이점이 없음
            result = sum(i * i for i in range(1000000))
            return result
        
        # ✅ 올바른 방법: executor 사용
        async def correct_cpu_intensive():
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None, 
                lambda: sum(i * i for i in range(1000000))
            )
            return result
        
        # ❌ 잘못된 방법: await 없이 코루틴 호출
        async def wrong_no_await():
            # correct_way()  # 코루틴 객체만 반환, 실행 안됨
            pass
        
        # ✅ 올바른 방법
        async def correct_with_await():
            await correct_way()  # 실제 실행
    
    async def exception_handling(self):
        """비동기에서의 예외 처리"""
        
        async def risky_operation():
            await asyncio.sleep(0.1)
            raise ValueError("의도적 오류")
        
        # 개별 태스크 예외 처리
        try:
            await risky_operation()
        except ValueError as e:
            print(f"예외 처리됨: {e}")
        
        # 여러 태스크의 예외 처리
        async def safe_task(task_id):
            try:
                if task_id == 2:
                    raise ValueError(f"Task {task_id} 오류")
                await asyncio.sleep(0.1)
                return f"Task {task_id} 성공"
            except Exception as e:
                return f"Task {task_id} 실패: {e}"
        
        tasks = [safe_task(i) for i in range(5)]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                print(f"Task {i} 예외: {result}")
            else:
                print(f"Task {i} 결과: {result}")

# 실행 예제
async def demonstrate_all():
    print("=== 리소스 효율성 데모 ===")
    resource_demo = ResourceEfficiency()
    resource_demo.compare_memory_usage()
    await resource_demo.demonstrate_scalability()
    
    print("\n=== 반응성 데모 ===")
    resp_demo = ResponsivenessDemo()
    await resp_demo.responsive_ui_simulation()
    await resp_demo.concurrent_background_tasks()
    
    print("\n=== 웹 크롤러 데모 ===")
    crawler = WebCrawlerExample()
    await crawler.async_web_crawler()
    
    print("\n=== 블록체인 활용 데모 ===")
    blockchain_demo = BlockchainAsyncUsage()
    await blockchain_demo.parallel_node_communication()

# 실행
# asyncio.run(demonstrate_all())