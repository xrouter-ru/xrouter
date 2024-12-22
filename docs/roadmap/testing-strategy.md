# XRouter Testing Strategy

## Overview

Комплексная стратегия тестирования XRouter охватывает все этапы разработки, от MVP до Production.

## MVP Testing (Python)

### Unit Tests
```python
# test_router.py
import pytest
from xrouter.router import Router

def test_route_selection():
    router = Router()
    request = ChatRequest(model="gigachat-pro")
    provider = router.select_provider(request)
    assert provider.name == "gigachat"

# test_provider.py
def test_gigachat_transform():
    provider = GigaChatProvider()
    request = ChatRequest(messages=[{"role": "user", "content": "Hi"}])
    transformed = provider.transform_request(request)
    assert transformed.prompt == "Hi"
```

### Integration Tests
```python
# test_integration.py
async def test_full_flow():
    client = TestClient(app)
    response = await client.post(
        "/v1/chat/completions",
        json={
            "model": "gigachat-pro",
            "messages": [{"role": "user", "content": "Hi"}]
        },
        headers={"Authorization": "Bearer test-token"}
    )
    assert response.status_code == 200
```

### Performance Tests
```python
# test_performance.py
from locust import HttpUser, task

class ApiUser(HttpUser):
    @task
    def chat_completion(self):
        self.client.post(
            "/v1/chat/completions",
            json={
                "model": "gigachat-pro",
                "messages": [{"role": "user", "content": "Hi"}]
            },
            headers={"Authorization": "Bearer test-token"}
        )
```

## Production Testing (Go)

### Unit Tests
```go
// router_test.go
func TestRouteSelection(t *testing.T) {
    router := NewRouter()
    request := &ChatRequest{Model: "gigachat-pro"}
    provider, err := router.SelectProvider(request)
    assert.NoError(t, err)
    assert.Equal(t, "gigachat", provider.Name())
}

// provider_test.go
func TestGigaChatTransform(t *testing.T) {
    provider := NewGigaChatProvider()
    request := &ChatRequest{
        Messages: []Message{{Role: "user", Content: "Hi"}},
    }
    transformed := provider.TransformRequest(request)
    assert.Equal(t, "Hi", transformed.Prompt)
}
```

### Integration Tests
```go
// integration_test.go
func TestFullFlow(t *testing.T) {
    server := NewTestServer()
    resp, err := server.Post("/v1/chat/completions", ChatRequest{
        Model: "gigachat-pro",
        Messages: []Message{{Role: "user", Content: "Hi"}},
    })
    assert.NoError(t, err)
    assert.Equal(t, 200, resp.StatusCode)
}
```

### Load Tests
```go
// loadtest.go
func BenchmarkChatCompletion(b *testing.B) {
    server := NewTestServer()
    for i := 0; i < b.N; i++ {
        server.Post("/v1/chat/completions", ChatRequest{
            Model: "gigachat-pro",
            Messages: []Message{{Role: "user", Content: "Hi"}},
        })
    }
}
```

## Test Categories

### Functional Testing
- API endpoints
- Provider integrations
- Authentication & Authorization
- Error handling
- Rate limiting

### Non-Functional Testing
- Performance
- Scalability
- Security
- Reliability
- Monitoring

### Security Testing
- Authentication tests
- Authorization tests
- Input validation
- Rate limiting
- Token handling

### Provider Testing
- Integration tests
- Error handling
- Fallback scenarios
- Version compatibility
- Token counting

## Test Environments

### Local
```yaml
environment:
  database: SQLite
  cache: Redis
  providers:
    gigachat: mock
    yandexgpt: mock
```

### Staging
```yaml
environment:
  database: PostgreSQL
  cache: Redis Cluster
  providers:
    gigachat: test account
    yandexgpt: test account
```

### Production
```yaml
environment:
  database: PostgreSQL HA
  cache: Redis Cluster
  providers:
    gigachat: prod account
    yandexgpt: prod account
```

## CI/CD Pipeline

### MVP (GitHub Actions)
```yaml
name: MVP Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
      - run: pip install -r requirements.txt
      - run: pytest
      - run: black --check .
      - run: isort --check .
```

### Production (Kubernetes)
```yaml
# Test Stage
stages:
  - test
  - build
  - deploy

test:
  stage: test
  script:
    - go test ./...
    - golangci-lint run
    - go test -bench=.
```

## Test Data Management

### Test Data Sets
```yaml
users:
  - id: test-user-1
    api_key: test-key-1
    tier: free
  - id: test-user-2
    api_key: test-key-2
    tier: pro

requests:
  - model: gigachat-pro
    messages:
      - role: user
        content: Test message 1
  - model: yandexgpt:latest
    messages:
      - role: user
        content: Test message 2
```

### Data Cleanup
```sql
-- Cleanup script
DELETE FROM usage_stats WHERE created_at < NOW() - INTERVAL '1 day';
DELETE FROM test_users WHERE id LIKE 'test-%';
```

## Monitoring & Reporting

### Test Metrics
- Test coverage
- Pass/fail rates
- Performance metrics
- Error distribution
- Test execution time

### Test Reports
```html
<!-- test-report.html -->
<report>
  <summary>
    <total>100</total>
    <passed>95</passed>
    <failed>5</failed>
    <coverage>85%</coverage>
  </summary>
  <details>
    <!-- Test details -->
  </details>
</report>
```

## Continuous Improvement

### Feedback Loop
1. Run tests
2. Collect metrics
3. Analyze results
4. Improve tests
5. Repeat

### Test Maintenance
- Regular review
- Update test data
- Improve coverage
- Optimize performance
- Update documentation