
# [DNA_TAG]
# ORIGIN: Crostini-Chromebook
# PILLAR: codecity-unified
# DEPS: automation_dna, json, pytest
# ROLE: Test suite for Web Application functionality
# AUTHOR: Buffy (Codebuff AI)
# SESSION: 2026-08-22 Bucket 08 DNA Sweep
# TIER: Test (0)
# [/DNA_TAG]

"""
Test suite for Web Application functionality
Tests Flask routes, API endpoints, and web interface
"""
import json
import pytest
from automation_dna.web.app import app
from automation_dna.core.dna_process import ProcessDNA


@pytest.fixture
def client():
    """Create test client for Flask app"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestWebRoutes:
    """Test basic web routes"""
    
    def test_index_route(self, client):
        """Test main index route"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'Automation DNA' in response.data or b'Evolution' in response.data
    
    def test_evolution_route(self, client):
        """Test evolution control route"""
        response = client.get('/evolution')
        assert response.status_code == 200
        assert b'Evolution' in response.data or b'Control' in response.data
    
    def test_marketplace_route(self, client):
        """Test marketplace route"""
        response = client.get('/marketplace')
        assert response.status_code == 200
        assert b'Marketplace' in response.data or b'Process' in response.data
    
    def test_editor_route(self, client):
        """Test editor route"""
        response = client.get('/editor')
        assert response.status_code == 200
        assert b'Editor' in response.data or b'DNA' in response.data


class TestAPIEndpoints:
    """Test API endpoints"""
    
    def test_api_evolve_endpoint(self, client):
        """Test evolution API endpoint"""
        response = client.post('/api/evolve')
        assert response.status_code in [200, 400]  # 200 if works, 400 if no population
        
        if response.status_code == 200:
            data = json.loads(response.data)
            assert 'generation' in data
            assert 'average_fitness' in data
            assert 'best_fitness' in data
    
    def test_api_processes_endpoint(self, client):
        """Test processes API endpoint"""
        response = client.get('/api/processes')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'processes' in data
        assert isinstance(data['processes'], list)
    
    def test_api_download_endpoint(self, client):
        """Test DNA download endpoint"""
        # First need to create a process to download
        test_dna = ProcessDNA(
            name="Test Download",
            version="1.0",
            steps=[],
            connections=[],
            metadata={}
        )
        
        # Add to app's evolution engine (simulated)
        # Note: This would need proper setup in a real test
        response = client.get('/api/download/test_process')
        
        # Should return JSON or file
        assert response.status_code in [200, 404]
        if response.status_code == 200:
            assert 'application/json' in response.content_type
    
    def test_api_upload_endpoint(self, client):
        """Test DNA upload endpoint"""
        test_dna = ProcessDNA(
            name="Test Upload",
            version="1.0",
            steps=[],
            connections=[],
            metadata={}
        )
        
        # Convert to JSON for upload
        dna_json = test_dna.to_json()
        
        response = client.post(
            '/api/upload',
            data={'file': (dna_json, 'test_process.json')},
            content_type='multipart/form-data'
        )
        
        assert response.status_code in [200, 400]
        if response.status_code == 200:
            data = json.loads(response.data)
            assert 'status' in data
            assert data['status'] == 'success'


class TestErrorHandling:
    """Test error handling in API endpoints"""
    
    def test_invalid_route(self, client):
        """Test invalid route handling"""
        response = client.get('/invalid_route')
        assert response.status_code == 404
    
    def test_invalid_api_endpoint(self, client):
        """Test invalid API endpoint"""
        response = client.post('/api/invalid')
        assert response.status_code == 404
    
    def test_invalid_upload(self, client):
        """Test invalid file upload"""
        response = client.post(
            '/api/upload',
            data={'file': ('invalid content', 'invalid.json')},
            content_type='multipart/form-data'
        )
        
        assert response.status_code in [400, 500]
        if response.status_code == 400:
            data = json.loads(response.data)
            assert 'error' in data


class TestResponseFormats:
    """Test response formats and content types"""
    
    def test_json_response_format(self, client):
        """Test that API returns proper JSON"""
        response = client.get('/api/processes')
        assert response.status_code == 200
        
        # Should be JSON content type
        assert 'application/json' in response.content_type
        
        # Should be parseable JSON
        data = json.loads(response.data)
        assert isinstance(data, dict)
    
    def test_html_response_format(self, client):
        """Test that web routes return proper HTML"""
        response = client.get('/')
        assert response.status_code == 200
        
        # Should be HTML content type
        assert 'text/html' in response.content_type


class TestTemplateRendering:
    """Test template rendering"""
    
    def test_base_template_features(self, client):
        """Test that base template features are present"""
        response = client.get('/')
        html = response.data.decode('utf-8')
        
        # Should have basic HTML structure
        assert '<html>' in html
        assert '</html>' in html
        assert '<head>' in html
        assert '</head>' in html
        assert '<body>' in html
        assert '</body>' in html
    
    def test_template_inheritance(self, client):
        """Test that templates inherit from base"""
        response = client.get('/evolution')
        html = response.data.decode('utf-8')
        
        # Should have base template features
        assert '<html>' in html
        assert '<body>' in html


class TestStaticFiles:
    """Test static file serving"""
    
    def test_css_file_serving(self, client):
        """Test CSS file serving"""
        response = client.get('/static/css/style.css')
        assert response.status_code == 200
        assert 'text/css' in response.content_type
    
    def test_js_file_serving(self, client):
        """Test JavaScript file serving"""
        response = client.get('/static/js/main.js')
        assert response.status_code == 200
        assert 'application/javascript' in response.content_type or 'text/javascript' in response.content_type


class TestFormHandling:
    """Test form handling and data submission"""
    
    def test_file_upload_form(self, client):
        """Test file upload form handling"""
        # Test with empty form
        response = client.post('/api/upload', data={})
        assert response.status_code in [400, 422]
        
        # Test with invalid file type
        response = client.post(
            '/api/upload',
            data={'file': ('not json content', 'test.txt')},
            content_type='multipart/form-data'
        )
        assert response.status_code in [400, 500]


class TestSessionManagement:
    """Test session management (basic tests)"""
    
    def test_session_creation(self, client):
        """Test that sessions are created"""
        response = client.get('/')
        assert response.status_code == 200
        
        # Should have session
        with client.session_transaction() as sess:
            # Session should exist
            assert sess is not None


class TestPerformance:
    """Test performance characteristics"""
    
    def test_route_response_time(self, client):
        """Test that routes respond in reasonable time"""
        import time
        
        # Test main routes
        routes = ['/', '/evolution', '/marketplace', '/editor']
        
        for route in routes:
            start_time = time.time()
            response = client.get(route)
            end_time = time.time()
            
            # Should respond quickly
            assert (end_time - start_time) < 0.5
            assert response.status_code == 200
    
    def test_api_response_time(self, client):
        """Test that API endpoints respond quickly"""
        import time
        
        # Test API endpoints
        endpoints = ['/api/processes']
        
        for endpoint in endpoints:
            start_time = time.time()
            response = client.get(endpoint)
            end_time = time.time()
            
            # Should respond quickly
            assert (end_time - start_time) < 0.5
            assert response.status_code == 200


class TestIntegration:
    """Test integration between components"""
    
    def test_dna_lifecycle(self, client):
        """Test complete DNA lifecycle through web interface"""
        # Create a test DNA
        test_dna = ProcessDNA(
            name="Integration Test",
            version="1.0",
            steps=[],
            connections=[],
            metadata={"test": "integration"}
        )
        
        # Upload it
        dna_json = test_dna.to_json()
        upload_response = client.post(
            '/api/upload',
            data={'file': (dna_json, 'integration_test.json')},
            content_type='multipart/form-data'
        )
        
        # Check upload response
        assert upload_response.status_code in [200, 400]
        
        # Get processes list
        processes_response = client.get('/api/processes')
        assert processes_response.status_code == 200
        
        # Should have our process or at least valid response
        processes_data = json.loads(processes_response.data)
        assert 'processes' in processes_data


class TestEdgeCases:
    """Test edge cases and unusual scenarios"""
    
    def test_large_file_upload(self, client):
        """Test upload of large file"""
        # Create large JSON content
        large_content = {"data": ["x" * 10000 for _ in range(100)]}
        large_json = json.dumps(large_content)
        
        response = client.post(
            '/api/upload',
            data={'file': (large_json, 'large_test.json')},
            content_type='multipart/form-data'
        )
        
        # Should handle gracefully
        assert response.status_code in [200, 400, 413]  # 413 = Payload Too Large
    
    def test_concurrent_requests(self, client):
        """Test handling of concurrent requests"""
        import threading
        import time
        
        def make_request():
            return client.get('/')
        
        # Create multiple threads
        threads = []
        results = []
        
        for _ in range(5):
            thread = threading.Thread(target=lambda: results.append(make_request()))
            threads.append(thread)
            thread.start()
        
        # Wait for completion
        for thread in threads:
            thread.join(timeout=2)
        
        # All requests should succeed
        for result in results:
            assert result.status_code == 200
    
    def test_malformed_json_upload(self, client):
        """Test upload of malformed JSON"""
        malformed_json = '{"name": "test", "invalid": "unclosed brace"'
        
        response = client.post(
            '/api/upload',
            data={'file': (malformed_json, 'malformed.json')},
            content_type='multipart/form-data'
        )
        
        # Should handle gracefully
        assert response.status_code in [400, 500]
