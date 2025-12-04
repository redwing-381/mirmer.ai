# Implementation Plan

- [x] 1. Implement model tier configuration system
  - Add MODEL_TIER environment variable support to config.py
  - Define MODEL_TIERS dictionary with speed/balanced/cost configurations
  - Implement get_model_config() function to select tier
  - Update COUNCIL_MODELS and CHAIRMAN_MODEL to use tier configuration
  - Add validation for invalid tier values with fallback to "balanced"
  - _Requirements: 2.3, 2.5_

- [ ]* 1.1 Write property test for model configuration
  - **Property 4: Model configuration via environment**
  - **Validates: Requirements 2.3**

- [x] 2. Implement adaptive rate limiter
  - Create backend/rate_limiter.py with AdaptiveRateLimiter class
  - Implement wait_if_needed() method with provider-specific tracking
  - Implement update_from_headers() to parse rate limit headers
  - Implement handle_rate_limit_error() with exponential backoff
  - Add jitter to backoff delays to prevent thundering herd
  - _Requirements: 1.4, 3.2, 3.4, 3.5_

- [ ]* 2.1 Write property test for exponential backoff
  - **Property 3: Exponential backoff on rate limits**
  - **Validates: Requirements 1.4, 3.5**

- [ ]* 2.2 Write property test for adaptive rate limiting
  - **Property 7: Adaptive rate limiting**
  - **Validates: Requirements 3.2, 3.4**

- [x] 3. Implement performance monitoring system
  - Create backend/performance.py with PerformanceMonitor class
  - Implement start_stage() and end_stage() for timing measurement
  - Implement log_model_response() for per-model timing
  - Implement get_statistics() for percentile calculation (p50, p90, p95, p99)
  - Implement check_performance_threshold() with stage-specific thresholds
  - _Requirements: 5.1, 5.2, 5.3, 5.4_

- [ ]* 3.1 Write property test for percentile calculation
  - **Property 13: Percentile statistics calculation**
  - **Validates: Requirements 5.4**

- [ ]* 3.2 Write unit tests for performance monitoring
  - Test timing measurement accuracy
  - Test threshold warning logic
  - Test metric aggregation
  - _Requirements: 5.1, 5.2, 5.3_

- [x] 4. Optimize council.py rate limiting
  - Remove or minimize artificial delays in stage1_collect_responses()
  - Remove or minimize artificial delays in stage2_collect_rankings()
  - Remove or minimize artificial delays in stage3_synthesize_final()
  - Integrate AdaptiveRateLimiter into council orchestration
  - Add rate limit header extraction from OpenRouter responses
  - _Requirements: 3.1, 3.2_

- [ ]* 4.1 Write property test for minimal delays
  - **Property 6: Minimal artificial delays**
  - **Validates: Requirements 3.1**

- [x] 5. Add performance monitoring to council.py
  - Integrate PerformanceMonitor into council orchestration
  - Add timing instrumentation to stage1_collect_responses()
  - Add timing instrumentation to stage2_collect_rankings()
  - Add timing instrumentation to stage3_synthesize_final()
  - Log per-model response times
  - Log stage completion times with threshold checks
  - _Requirements: 5.1, 5.2, 5.3_

- [ ]* 5.1 Write property test for complete logging
  - **Property 11: Complete performance logging**
  - **Validates: Requirements 5.1, 5.2**

- [ ]* 5.2 Write property test for threshold warnings
  - **Property 12: Performance threshold warnings**
  - **Validates: Requirements 5.3**

- [ ] 6. Implement graceful degradation for model failures
  - Update stage1_collect_responses() to continue with partial results
  - Update stage2_collect_rankings() to handle missing models
  - Update stage3_synthesize_final() to work with incomplete data
  - Add minimum threshold check (require at least 2 successful models)
  - Log all model failures with context
  - _Requirements: 2.4_

- [ ]* 6.1 Write property test for graceful degradation
  - **Property 5: Graceful degradation on model failure**
  - **Validates: Requirements 2.4**

- [ ] 7. Optimize streaming behavior
  - Update council.py to emit SSE events immediately when responses arrive
  - Implement progressive streaming for Stage 1 responses
  - Implement progressive streaming for Stage 2 rankings
  - Add stage completion events with timestamps
  - Ensure event ordering is maintained
  - _Requirements: 4.1, 4.2, 4.4, 4.5_

- [ ]* 7.1 Write property test for progressive streaming
  - **Property 8: Progressive streaming**
  - **Validates: Requirements 4.1, 4.2, 4.5**

- [ ]* 7.2 Write property test for stream event ordering
  - **Property 10: Stream event ordering**
  - **Validates: Requirements 4.4**

- [ ] 8. Implement early stage transition
  - Modify stage2_collect_rankings() to signal when 50% complete
  - Update council orchestration to start Stage 3 early when possible
  - Add logic to determine "sufficient data" threshold
  - Ensure Stage 3 waits for minimum required rankings
  - _Requirements: 4.3_

- [ ]* 8.1 Write property test for early stage transition
  - **Property 9: Early stage transition**
  - **Validates: Requirements 4.3**

- [ ] 9. Add timeout handling
  - Implement per-model timeout in openrouter.py (10 seconds)
  - Implement chairman timeout in stage3_synthesize_final() (15 seconds)
  - Handle timeout exceptions as model failures
  - Log timeout events for monitoring
  - _Requirements: 2.4_

- [ ] 10. Update environment configuration
  - Add MODEL_TIER to .env.example with documentation
  - Document available tiers (speed, balanced, cost) in README
  - Add performance targets for each tier
  - Add cost estimates for each tier
  - Update deployment documentation
  - _Requirements: 2.3, 6.1, 6.2, 6.3, 6.4_

- [ ] 11. Add startup validation
  - Implement model configuration validation at startup
  - Check that selected models are valid OpenRouter model IDs
  - Log selected tier and expected performance
  - Warn if using cost tier in production
  - _Requirements: 5.5_

- [ ] 12. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ]* 13. Integration testing
  - Test end-to-end latency with speed tier
  - Test end-to-end latency with balanced tier
  - Verify 90th percentile meets targets
  - Test concurrent query handling
  - Measure actual cost per query
  - _Requirements: 1.1, 1.2, 1.5_

- [ ]* 13.1 Write property test for latency improvement
  - **Property 1: Latency improvement**
  - **Validates: Requirements 1.1, 1.2**

- [ ]* 13.2 Write property test for concurrent performance
  - **Property 2: Concurrent query performance**
  - **Validates: Requirements 1.5**

- [ ] 14. Documentation and deployment
  - Update README with performance optimization details
  - Document model tier selection strategy
  - Add performance monitoring guide
  - Create migration guide for existing deployments
  - Update cost analysis documentation
  - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5_

- [ ] 15. Final checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.
