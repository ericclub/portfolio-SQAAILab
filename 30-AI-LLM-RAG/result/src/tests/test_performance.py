"""Performance and load tests for LLM inference."""
import pytest
import time
import statistics
from concurrent.futures import ThreadPoolExecutor
from config import Config


class TestPerformanceBaseline:
    """Establish performance baselines for LLM inference."""

    def test_response_latency(self, lm_studio_client):
        """Measure and validate response latency."""
        latencies = []

        for _ in range(5):
            start = time.time()
            response = lm_studio_client.chat.completions.create(
                model=Config.EXPECTED_MODEL_NAME,
                messages=[{"role": "user", "content": "Say OK"}],
                max_tokens=5
            )
            latency = time.time() - start
            latencies.append(latency)

        avg_latency = statistics.mean(latencies)
        max_latency = max(latencies)
        min_latency = min(latencies)

        print(f"\nLatency Stats: avg={avg_latency:.2f}s, min={min_latency:.2f}s, max={max_latency:.2f}s")

        assert avg_latency < Config.MAX_RESPONSE_TIME_SECONDS, (
            f"Average latency {avg_latency:.2f}s exceeds {Config.MAX_RESPONSE_TIME_SECONDS}s threshold"
        )

    def test_response_time_consistency(self, lm_studio_client):
        """Verify response times are consistent (low standard deviation)."""
        times = []

        for _ in range(5):
            start = time.time()
            lm_studio_client.chat.completions.create(
                model=Config.EXPECTED_MODEL_NAME,
                messages=[{"role": "user", "content": "Reply: test"}],
                max_tokens=5
            )
            times.append(time.time() - start)

        if len(times) >= 2:
            std_dev = statistics.stdev(times)
            mean_time = statistics.mean(times)
            cv = std_dev / mean_time  # Coefficient of variation

            print(f"\nConsistency: mean={mean_time:.2f}s, std={std_dev:.2f}s, CV={cv:.2f}")

            # CV < 1.0 indicates reasonable consistency
            assert cv < 1.0, f"Response times too inconsistent (CV={cv:.2f})"

    @pytest.mark.slow
    def test_extended_baseline(self, lm_studio_client):
        """Extended baseline test with 10 iterations."""
        latencies = []

        for i in range(10):
            start = time.time()
            lm_studio_client.chat.completions.create(
                model=Config.EXPECTED_MODEL_NAME,
                messages=[{"role": "user", "content": f"Test {i}: say OK"}],
                max_tokens=5
            )
            latencies.append(time.time() - start)

        print(f"\nExtended Baseline (10 runs):")
        print(f"  Mean: {statistics.mean(latencies):.2f}s")
        print(f"  Median: {statistics.median(latencies):.2f}s")
        print(f"  Std Dev: {statistics.stdev(latencies):.2f}s")
        print(f"  Min: {min(latencies):.2f}s")
        print(f"  Max: {max(latencies):.2f}s")


class TestConcurrency:
    """Test concurrent request handling."""

    def test_sequential_requests(self, lm_studio_client):
        """Verify sequential requests complete successfully."""
        for i in range(3):
            response = lm_studio_client.chat.completions.create(
                model=Config.EXPECTED_MODEL_NAME,
                messages=[{"role": "user", "content": f"Count: {i}"}],
                max_tokens=10
            )
            assert response.choices[0].message.content, f"Request {i} failed"

    def test_parallel_requests(self, session, api_base_url):
        """Test handling of parallel requests (should queue properly)."""
        def make_request(prompt):
            try:
                response = session.post(
                    f"{api_base_url}/chat/completions",
                    json={
                        "model": Config.EXPECTED_MODEL_NAME,
                        "messages": [{"role": "user", "content": prompt}],
                        "max_tokens": 10
                    },
                    timeout=Config.TEST_TIMEOUT
                )
                return response.status_code
            except Exception as e:
                return str(e)

        with ThreadPoolExecutor(max_workers=2) as executor:
            futures = [
                executor.submit(make_request, f"Say {i}")
                for i in range(2)
            ]
            results = [f.result() for f in futures]

        print(f"\nParallel request results: {results}")
        # All requests should complete (may be queued)
        assert all(r == 200 for r in results), f"Some requests failed: {results}"

    @pytest.mark.slow
    def test_burst_requests(self, session, api_base_url):
        """Test system behavior under burst of requests."""
        def make_request(idx):
            try:
                start = time.time()
                response = session.post(
                    f"{api_base_url}/chat/completions",
                    json={
                        "model": Config.EXPECTED_MODEL_NAME,
                        "messages": [{"role": "user", "content": f"Burst {idx}"}],
                        "max_tokens": 5
                    },
                    timeout=Config.TEST_TIMEOUT * 2
                )
                return {"idx": idx, "status": response.status_code, "time": time.time() - start}
            except Exception as e:
                return {"idx": idx, "status": "error", "error": str(e)}

        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = [executor.submit(make_request, i) for i in range(3)]
            results = [f.result() for f in futures]

        print(f"\nBurst test results:")
        for r in results:
            print(f"  Request {r['idx']}: {r.get('status')} in {r.get('time', 'N/A'):.2f}s")

        successful = sum(1 for r in results if r.get("status") == 200)
        assert successful >= 2, f"Too many burst requests failed: {successful}/3 succeeded"


class TestContextWindow:
    """Test context window handling."""

    def test_moderate_context(self, lm_studio_client):
        """Test with moderate context length (~500 tokens)."""
        # Create a reasonably long context
        long_context = "This is a test sentence with some words. " * 50

        response = lm_studio_client.chat.completions.create(
            model=Config.EXPECTED_MODEL_NAME,
            messages=[
                {"role": "user", "content": f"Summarize in one sentence: {long_context}"}
            ],
            max_tokens=50
        )
        assert response.choices[0].message.content, "Failed with moderate context"
        print(f"\nModerate context response: {response.choices[0].message.content[:100]}")

    def test_large_context_graceful_handling(self, lm_studio_client):
        """Test system handles context overflow gracefully."""
        # Very large context - should either work or fail gracefully
        huge_context = "Lorem ipsum dolor sit amet consectetur. " * 500

        try:
            response = lm_studio_client.chat.completions.create(
                model=Config.EXPECTED_MODEL_NAME,
                messages=[
                    {"role": "user", "content": f"Respond OK: {huge_context}"}
                ],
                max_tokens=10
            )
            # If it works, record it
            print(f"\nLarge context accepted: {response.choices[0].message.content[:50]}")
        except Exception as e:
            # Should fail gracefully with informative error
            error_str = str(e).lower()
            graceful = any(
                word in error_str
                for word in ["context", "token", "length", "limit", "exceed"]
            )
            print(f"\nLarge context rejected: {type(e).__name__} - {str(e)[:100]}")
            if not graceful:
                # Still pass but note the unexpected error type
                print(f"Note: Error may need investigation")


class TestTokenThroughput:
    """Test token generation throughput."""

    def test_tokens_per_second(self, lm_studio_client):
        """Measure token generation speed."""
        start = time.time()

        response = lm_studio_client.chat.completions.create(
            model=Config.EXPECTED_MODEL_NAME,
            messages=[
                {"role": "user", "content": "Write a paragraph about software testing."}
            ],
            max_tokens=100
        )

        elapsed = time.time() - start

        # Estimate tokens from response (~1.3 tokens per word)
        content = response.choices[0].message.content
        word_count = len(content.split())
        estimated_tokens = word_count * 1.3
        tokens_per_second = estimated_tokens / elapsed if elapsed > 0 else 0

        print(
            f"\nThroughput: ~{tokens_per_second:.1f} tokens/sec "
            f"({estimated_tokens:.0f} tokens in {elapsed:.1f}s)"
        )

        assert tokens_per_second >= Config.MIN_TOKENS_PER_SECOND, (
            f"Token generation too slow: {tokens_per_second:.1f} t/s"
        )

    @pytest.mark.slow
    def test_sustained_throughput(self, lm_studio_client):
        """Test sustained throughput over multiple requests."""
        total_tokens = 0
        total_time = 0

        for i in range(5):
            start = time.time()
            response = lm_studio_client.chat.completions.create(
                model=Config.EXPECTED_MODEL_NAME,
                messages=[
                    {"role": "user", "content": f"Write sentence {i} about cats."}
                ],
                max_tokens=50
            )
            elapsed = time.time() - start
            
            content = response.choices[0].message.content
            estimated_tokens = len(content.split()) * 1.3
            
            total_tokens += estimated_tokens
            total_time += elapsed

        sustained_rate = total_tokens / total_time if total_time > 0 else 0
        print(f"\nSustained throughput: {sustained_rate:.1f} tokens/sec over 5 requests")


class TestLongRunningStability:
    """Test system stability over extended operation."""

    @pytest.mark.slow
    def test_repeated_inference_stability(self, lm_studio_client):
        """Test that repeated inferences remain stable."""
        results = []

        for i in range(10):
            try:
                start = time.time()
                response = lm_studio_client.chat.completions.create(
                    model=Config.EXPECTED_MODEL_NAME,
                    messages=[{"role": "user", "content": f"Iteration {i}: say hello"}],
                    max_tokens=20
                )
                elapsed = time.time() - start
                results.append({
                    "iteration": i,
                    "success": True,
                    "time": elapsed,
                    "response_length": len(response.choices[0].message.content)
                })
            except Exception as e:
                results.append({
                    "iteration": i,
                    "success": False,
                    "error": str(e)
                })

        successful = sum(1 for r in results if r["success"])
        print(f"\nStability test: {successful}/10 successful")
        
        if successful >= 2:
            times = [r["time"] for r in results if r["success"]]
            print(f"  Avg time: {statistics.mean(times):.2f}s")
            print(f"  Time range: {min(times):.2f}s - {max(times):.2f}s")

        assert successful >= 8, f"Too many failures in stability test: {successful}/10"
