# Performance Optimization Design Document

## Overview

This design document outlines the architecture and implementation strategy for optimizing the Mirmer AI multi-LLM consultation system's response time. The current system takes approximately 30 seconds to complete the 3-stage council process. This optimization will reduce latency to under 15 seconds while maintaining response quality and managing costs effectively.

The optimization strategy focuses on three key areas:
1. **Model Selection**: Upgrading to faster, more capable models
2. **Rate Limiting Optimization**: Removing unnecessary delays and implementing intelligent rate limit handling
3. **Streaming Improvements**: Ensuring progressive updates reach users as quickly as possible

## Architecture

### Current Architecture Analysis

The current system has the following performance characteristics:

**Stage 1 (Parallel Model Queries)**
- 4 models queried in parallel: GPT-3.5-turbo, Claude Haiku, Mistral-7B, Llama-3.1-8B
- 1-second artificial delay before queries
- Estimated 5-8 seconds for model inference (slower models)

**Stage 2 (Peer Rankings)**
- Same 4 models rank responses in parallel
- 2-second artificial delay before queries
- Estimated 5-8 seconds for ranking generation

**Stage 3 (Chairman Synthesis)**
- Single chairman model (Claude Haiku)
- 2-second artificial delay before query
- Estimated 5-8 seconds for synthesis

**Total Time**: ~5s (delays) + ~18-24s (inference) = 23-29 seconds

### Optimized Architecture

The optimized architecture will:

1. **Upgrade to faster models** with sub-3-second inference times
2. **Remove or minimize artificial delays** (currently 5 seconds total)
3. **Implement adaptive rate limiting** based on actual API responses
4. **Optimize streaming** to deliver results as soon as available
5. **Add performance monitoring** to track improvements

### Model Tier Strategy

We'll implement a tiered model selection strategy:

**Tier 1: Speed-Optimized (Target: <15s total)**
- Council: GPT-4o-mini, Claude 3.5 Haiku, Gemini 1.5 Flash, Llama 3.3 70B
- Chairman: Claude 3.5 Sonnet or GPT-4o
- Cost: ~$0.015-0.025 per query
- Target latency: 10-15 seconds

**Tier 2: Balanced (Target: <20s total)**
- Council: GPT-4o-mini, Claude 3 Haiku, Gemini Flash, Mistral Small
- Chairman: Claude 3.5 Haiku
- Cost: ~$0.008-0.015 per query
- Target latency: 15-20 seconds

**Tier 3: Cost-Optimized (Current)**
- Council: GPT-3.5-turbo, Claude 3 Haiku, Mistral-7B, Llama-3.1-8B
- Chairman: Claude 3 Haiku
- Cost: ~$0.005-0.010 per query
- Current latency: 25-30 seconds

## Components and Interfaces

### 1. Model Configuration Module

**File**: `backend/config.py`

**Changes**:
```python
# Add model tier configuration
MODEL_TIER = os.getenv("MODEL_TIER", "balanced")  # speed, balanced, cost

# Model configurations by tier
MODEL_TIERS = {
    "speed": {
        "council": [
            "openai/gpt-4o-mini",
            "anthropic/claude-3-5-haiku",
            "google/gemini-1.5-flash",
            "meta-llama/llama-3.3-70b-instruct"
        ],
        "chairman": "anthropic/claude-3-5-sonnet",
        "expected_latency": 12,  # seconds
        "cost_per_query": 0.020
    },
    "balanced": {
        "council": [
            "openai/gpt-4o-mini",
            "anthropic/claude-3-haiku",
            "google/gemini-flash-1.5",
            "mistralai/mistral-small"
        ],
        "chairman": "anthropic/claude-3-5-haiku",
        "expected_latency": 18,  # seconds
        "cost_per_query": 0.012
    },
    "cost": {
        "council": [
            "openai/gpt-3.5-turbo",
            "anthropic/claude-3-haiku",
            "mistralai/mistral-7b-instruct",
            "meta-llama/llama-3.1-8b-instruct"
        ],
        "chairman": "anthropic/claude-3-haiku",
        "expected_latency": 27,  # seconds
        "cost_per_query": 0.008
    }
}

# Get current tier configuration
def get_model_config():
    tier = MODEL_TIER
    if tier not in MODEL_TIERS:
        logger.warning(f"Invalid MODEL_TIER '{tier}', defaulting to 'balanced'")
        tier = "balanced"
    return MODEL_TIERS[tier]

COUNCIL_MODELS = get_model_config()["council"]
CHAIRMAN_MODEL = get_model_config()["chairman"]
```

### 2. Rate Limiting Module

**File**: `backend/rate_limiter.py` (new)

**Purpose**: Intelligent rate limiting based on actual API responses

**Interface**:
```python
class AdaptiveRateLimiter:
    """
    Manages rate limiting with adaptive delays based on API responses.
    """
    
    def __init__(self):
        self.last_request_time = {}
        self.rate_limit_info = {}
    
    async def wait_if_needed(self, provider: str) -> None:
        """
        Wait if necessary to respect rate limits for a provider.
        Uses actual rate limit headers when available.
        """
        pass
    
    def update_from_headers(self, provider: str, headers: dict) -> None:
        """
        Update rate limit info from API response headers.
        """
        pass
    
    async def handle_rate_limit_error(self, provider: str, retry_count: int) -> None:
        """
        Handle rate limit errors with exponential backoff.
        """
        pass
```

### 3. Performance Monitoring Module

**File**: `backend/performance.py` (new)

**Purpose**: Track and log performance metrics

**Interface**:
```python
class PerformanceMonitor:
    """
    Tracks timing metrics for the 3-stage council process.
    """
    
    def __init__(self):
        self.metrics = []
    
    def start_stage(self, stage: int, context: dict) -> str:
        """
        Start timing a stage. Returns a timer ID.
        """
        pass
    
    def end_stage(self, timer_id: str) -> float:
        """
        End timing a stage. Returns elapsed time in seconds.
        """
        pass
    
    def log_model_response(self, model: str, duration: float) -> None:
        """
        Log individual model response time.
        """
        pass
    
    def get_statistics(self) -> dict:
        """
        Calculate aggregate statistics (p50, p90, p95, p99).
        """
        pass
    
    def check_performance_threshold(self, stage: int, duration: float) -> None:
        """
        Log warning if stage exceeds expected threshold.
        """
        pass
```

### 4. Enhanced Council Orchestration

**File**: `backend/council.py`

**Changes**:
- Remove or minimize artificial delays
- Add performance monitoring
- Implement adaptive rate limiting
- Optimize streaming behavior

## Data Models

### Performance Metrics Model

```python
@dataclass
class StageMetrics:
    stage: int
    start_time: float
    end_time: float
    duration: float
    model_timings: Dict[str, float]
    success_count: int
    failure_count: int
```

### Rate Limit Info Model

```python
@dataclass
class RateLimitInfo:
    provider: str
    requests_remaining: Optional[int]
    requests_limit: Optional[int]
    reset_time: Optional[float]
    last_updated: float
```

### Model Configuration Model

```python
@dataclass
class ModelConfig:
    tier: str
    council_models: List[str]
    chairman_model: str
    expected_latency: float
    cost_per_query: float
```


## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property Reflection

After analyzing all acceptance criteria, several properties can be consolidated:
- Properties 1.1 and 1.2 both test latency improvements and can be combined into a single comprehensive latency property
- Properties 4.1 and 4.2 both test progressive streaming and can be combined
- Properties 5.1 and 5.2 both test logging completeness and can be combined
- Properties related to rate limiting (1.4, 3.2, 3.4, 3.5) can be consolidated into comprehensive rate limit handling properties

### Property 1: Latency improvement

*For any* user query, the total time from submission to final response completion should be under 15 seconds for at least 90% of queries, representing at least a 50% improvement over the 30-second baseline.
**Validates: Requirements 1.1, 1.2**

### Property 2: Concurrent query performance

*For any* set of concurrent queries, processing multiple queries simultaneously should not cause individual query latency to exceed 120% of single-query latency.
**Validates: Requirements 1.5**

### Property 3: Exponential backoff on rate limits

*For any* sequence of rate limit errors, retry delays should follow exponential backoff pattern starting at 1 second (1s, 2s, 4s, 8s, etc.).
**Validates: Requirements 1.4, 3.5**

### Property 4: Model configuration via environment

*For any* valid MODEL_TIER environment variable value (speed, balanced, cost), the system should load the corresponding council and chairman models from the configuration.
**Validates: Requirements 2.3**

### Property 5: Graceful degradation on model failure

*For any* query where one or more council models fail, the system should complete the 3-stage process using the remaining successful model responses rather than failing completely.
**Validates: Requirements 2.4**

### Property 6: Minimal artificial delays

*For any* query execution, the total artificial delay time (sleep/wait calls not related to rate limiting) should be less than 1 second across all three stages.
**Validates: Requirements 3.1**

### Property 7: Adaptive rate limiting

*For any* API response containing rate limit headers (X-RateLimit-Remaining, X-RateLimit-Reset), the system should adjust subsequent request timing based on those headers rather than using fixed delays.
**Validates: Requirements 3.2, 3.4**

### Property 8: Progressive streaming

*For any* query, when a Stage 1 response or Stage 2 ranking completes, the system should emit a stream event for that result within 100 milliseconds, rather than waiting for all results in that stage.
**Validates: Requirements 4.1, 4.2, 4.5**

### Property 9: Early stage transition

*For any* query, Stage 3 should begin as soon as Stage 2 has at least 50% of rankings available, rather than waiting for all rankings to complete.
**Validates: Requirements 4.3**

### Property 10: Stream event ordering

*For any* query, streamed events should maintain correct chronological ordering with stage numbers (1, 2, 3) and within-stage sequence numbers increasing monotonically.
**Validates: Requirements 4.4**

### Property 11: Complete performance logging

*For any* query, the system should log timing metrics that include: total duration, per-stage durations, and per-model response times for all models that responded.
**Validates: Requirements 5.1, 5.2**

### Property 12: Performance threshold warnings

*For any* stage execution that exceeds the expected threshold (Stage 1: 5s, Stage 2: 5s, Stage 3: 7s), the system should emit a warning log entry.
**Validates: Requirements 5.3**

### Property 13: Percentile statistics calculation

*For any* collection of timing measurements, the calculated percentile statistics (p50, p90, p95, p99) should correctly represent the distribution of values.
**Validates: Requirements 5.4**

## Error Handling

### Rate Limit Errors

**Strategy**: Exponential backoff with jitter
- First retry: 1 second + random(0-0.5s)
- Second retry: 2 seconds + random(0-1s)
- Third retry: 4 seconds + random(0-2s)
- Maximum retries: 5
- After max retries: Return partial results if available, otherwise error

### Model Failure Handling

**Strategy**: Graceful degradation
- If 1 model fails: Continue with 3 models
- If 2 models fail: Continue with 2 models
- If 3+ models fail: Return error to user with explanation
- Log all failures for monitoring

### Timeout Handling

**Strategy**: Per-stage timeouts
- Stage 1: 10-second timeout per model (parallel)
- Stage 2: 10-second timeout per model (parallel)
- Stage 3: 15-second timeout for chairman
- On timeout: Treat as model failure, continue with available results

### Configuration Errors

**Strategy**: Fail fast with clear messages
- Invalid MODEL_TIER: Log warning, default to "balanced"
- Missing API key: Fail at startup with clear error
- Invalid model names: Validate at startup, fail if none are valid

## Testing Strategy

### Unit Testing

We'll use pytest for unit testing with the following focus areas:

**Configuration Module Tests**:
- Test model tier selection (speed, balanced, cost)
- Test environment variable parsing
- Test default fallback behavior
- Test model configuration validation

**Rate Limiter Tests**:
- Test exponential backoff calculation
- Test rate limit header parsing
- Test adaptive delay calculation
- Test concurrent request handling

**Performance Monitor Tests**:
- Test timing measurement accuracy
- Test percentile calculation correctness
- Test threshold warning logic
- Test metric aggregation

### Property-Based Testing

We'll use Hypothesis (Python's property-based testing library) configured to run a minimum of 100 iterations per test. Each property-based test will be tagged with a comment explicitly referencing the correctness property from this design document using the format: **Feature: performance-optimization, Property {number}: {property_text}**

**Performance Properties**:
- Test latency improvements across random queries
- Test concurrent query handling with varying loads
- Test graceful degradation with random model failures

**Rate Limiting Properties**:
- Test exponential backoff with random error sequences
- Test adaptive rate limiting with random header values

**Streaming Properties**:
- Test progressive streaming with random response timing
- Test event ordering with random stage completion patterns

**Monitoring Properties**:
- Test percentile calculations with random timing data
- Test threshold warnings with random performance data

### Integration Testing

**End-to-End Performance Tests**:
- Measure actual latency with real API calls
- Verify 90th percentile under 15 seconds
- Test with different model tiers

**Streaming Integration Tests**:
- Verify SSE events arrive progressively
- Test frontend receives events in correct order
- Measure time-to-first-byte for each stage

### Load Testing

**Concurrent Query Tests**:
- Test 10, 50, 100 concurrent queries
- Measure latency degradation
- Verify rate limiting works correctly

## Implementation Notes

### Phase 1: Model Upgrade (Highest Impact)

1. Add model tier configuration to `config.py`
2. Update environment variables
3. Test with "speed" tier
4. Measure latency improvement

**Expected Impact**: 40-50% latency reduction

### Phase 2: Rate Limiting Optimization

1. Implement `AdaptiveRateLimiter` class
2. Remove artificial delays from `council.py`
3. Add rate limit header parsing
4. Implement exponential backoff

**Expected Impact**: 15-20% latency reduction

### Phase 3: Streaming Optimization

1. Modify council.py to stream results immediately
2. Update SSE event emission logic
3. Implement early stage transition
4. Test progressive updates

**Expected Impact**: 5-10% perceived latency reduction

### Phase 4: Monitoring

1. Implement `PerformanceMonitor` class
2. Add timing instrumentation to council.py
3. Add performance logging
4. Implement statistics calculation

**Expected Impact**: No latency change, enables ongoing optimization

## Performance Targets by Tier

### Speed Tier
- Stage 1: 2-3 seconds (4 models in parallel)
- Stage 2: 2-3 seconds (4 models in parallel)
- Stage 3: 3-5 seconds (chairman synthesis)
- **Total: 7-11 seconds** (target: <12s)

### Balanced Tier
- Stage 1: 3-5 seconds
- Stage 2: 3-5 seconds
- Stage 3: 4-6 seconds
- **Total: 10-16 seconds** (target: <18s)

### Cost Tier (Current)
- Stage 1: 5-8 seconds
- Stage 2: 5-8 seconds
- Stage 3: 5-8 seconds
- **Total: 15-24 seconds** (current: ~27s with delays)

## Migration Strategy

### Backward Compatibility

- Default to "balanced" tier if MODEL_TIER not set
- Existing environment variables continue to work
- No breaking changes to API contracts
- Frontend requires no changes

### Rollout Plan

1. **Week 1**: Deploy with "balanced" tier as default
2. **Week 2**: Monitor performance, adjust thresholds
3. **Week 3**: Enable "speed" tier for Pro users
4. **Week 4**: Optimize based on real-world metrics

### Monitoring and Rollback

- Track p50, p90, p95, p99 latencies
- Monitor error rates and model failures
- Set up alerts for latency regressions
- Keep ability to rollback to previous model configuration

## Cost Analysis

### Current Cost (Cost Tier)
- Council: 4 models × $0.002 = $0.008
- Chairman: $0.002
- **Total: ~$0.010 per query**

### Balanced Tier
- Council: 4 models × $0.003 = $0.012
- Chairman: $0.002
- **Total: ~$0.014 per query** (+40% cost)

### Speed Tier
- Council: 4 models × $0.004 = $0.016
- Chairman: $0.008
- **Total: ~$0.024 per query** (+140% cost)

### Business Impact

**Free Tier** (10 queries/day):
- Current: $0.10/user/day
- Balanced: $0.14/user/day (+$0.04)
- Speed: $0.24/user/day (+$0.14)

**Pro Tier** (100 queries/day):
- Current: $1.00/user/day
- Balanced: $1.40/user/day (+$0.40)
- Speed: $2.40/user/day (+$1.40)

**Recommendation**: Use "balanced" tier for all users initially, offer "speed" tier as premium add-on for Pro users willing to pay extra.
