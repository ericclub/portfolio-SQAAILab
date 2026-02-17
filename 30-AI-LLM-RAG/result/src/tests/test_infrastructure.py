"""Infrastructure and connectivity tests for LM Studio setup."""
import pytest
import socket
import subprocess
import requests
from config import Config


class TestNetworkConnectivity:
    """Test network connectivity to LM Studio server."""

    def test_tcp_port_reachable(self):
        """Verify TCP port 1234 is reachable on Gaming PC."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        result = sock.connect_ex((Config.LM_STUDIO_HOST, Config.LM_STUDIO_PORT))
        sock.close()
        assert result == 0, f"Port {Config.LM_STUDIO_PORT} not reachable on {Config.LM_STUDIO_HOST}"

    def test_ping_host(self):
        """Verify host is pingable (network layer)."""
        result = subprocess.run(
            ["ping", "-n", "1", "-w", "3000", Config.LM_STUDIO_HOST],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, f"Cannot ping {Config.LM_STUDIO_HOST}"


class TestAPIHealth:
    """Test LM Studio API health and availability."""

    def test_api_root_accessible(self, session, api_base_url):
        """Verify API root endpoint responds."""
        response = session.get(f"{api_base_url}/models")
        assert response.status_code == 200, f"API returned {response.status_code}"

    def test_models_endpoint_returns_list(self, session, api_base_url):
        """Verify /v1/models returns model list."""
        response = session.get(f"{api_base_url}/models")
        data = response.json()
        assert "data" in data, "Response missing 'data' field"
        assert isinstance(data["data"], list), "'data' should be a list"

    def test_expected_model_loaded(self, session, api_base_url):
        """Verify expected model is loaded and available."""
        response = session.get(f"{api_base_url}/models")
        data = response.json()
        model_ids = [m["id"] for m in data["data"]]

        # Check if any model contains expected name
        found = any(
            Config.EXPECTED_MODEL_NAME.lower() in m.lower() for m in model_ids
        )
        assert found, (
            f"Expected model '{Config.EXPECTED_MODEL_NAME}' not found. "
            f"Available: {model_ids}"
        )


class TestGPUStatus:
    """Test GPU availability and usage.
    
    Note: These tests should be run on the Gaming PC where the GPU is located.
    """

    @pytest.mark.gpu
    def test_gpu_detected(self):
        """Verify NVIDIA GPU is detected."""
        # Check if nvidia-smi is available
        where_result = subprocess.run(
            ["where", "nvidia-smi"],
            capture_output=True
        )
        if where_result.returncode != 0:
            pytest.skip("nvidia-smi not available - run this test on Gaming PC")

        result = subprocess.run(
            ["nvidia-smi", "--query-gpu=name", "--format=csv,noheader"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, "nvidia-smi failed"
        assert "RTX" in result.stdout or "GeForce" in result.stdout, (
            "No NVIDIA GPU detected"
        )

    @pytest.mark.gpu
    def test_gpu_memory_available(self):
        """Verify GPU has sufficient memory (>= 8GB)."""
        where_result = subprocess.run(
            ["where", "nvidia-smi"],
            capture_output=True
        )
        if where_result.returncode != 0:
            pytest.skip("nvidia-smi not available - run this test on Gaming PC")

        result = subprocess.run(
            ["nvidia-smi", "--query-gpu=memory.total", "--format=csv,noheader,nounits"],
            capture_output=True,
            text=True
        )
        total_memory = int(result.stdout.strip())
        assert total_memory >= 8000, (
            f"GPU memory {total_memory}MB is below 8GB minimum"
        )

    @pytest.mark.gpu
    def test_gpu_memory_usage_during_inference(self, lm_studio_client):
        """Verify GPU memory is used during inference.
        
        This test captures GPU memory before and after inference to verify
        the model is actually using GPU resources.
        """
        where_result = subprocess.run(
            ["where", "nvidia-smi"],
            capture_output=True
        )
        if where_result.returncode != 0:
            pytest.skip("nvidia-smi not available - run this test on Gaming PC")

        # Get initial GPU memory
        result_before = subprocess.run(
            ["nvidia-smi", "--query-gpu=memory.used", "--format=csv,noheader,nounits"],
            capture_output=True,
            text=True
        )
        memory_before = int(result_before.stdout.strip())

        # Run inference
        lm_studio_client.chat.completions.create(
            model=Config.EXPECTED_MODEL_NAME,
            messages=[{"role": "user", "content": "Write a 50 word paragraph."}],
            max_tokens=100
        )

        # Get GPU memory after
        result_after = subprocess.run(
            ["nvidia-smi", "--query-gpu=memory.used", "--format=csv,noheader,nounits"],
            capture_output=True,
            text=True
        )
        memory_after = int(result_after.stdout.strip())

        print(f"\nGPU Memory: Before={memory_before}MB, After={memory_after}MB")
        
        # Model should be using significant GPU memory
        assert memory_after > 1000, (
            f"GPU memory usage ({memory_after}MB) too low - model may not be on GPU"
        )
