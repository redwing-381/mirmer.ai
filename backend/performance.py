"""
Performance monitoring for the 3-stage council process.

Tracks timing metrics, calculates statistics, and logs performance warnings.
"""
import logging
import time
import uuid
from collections import defaultdict
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class PerformanceMonitor:
    """
    Tracks timing metrics for the 3-stage council process.
    
    Features:
    - Stage-level timing (start/end)
    - Per-model response timing
    - Percentile statistics (p50, p90, p95, p99)
    - Performance threshold warnings
    """
    
    # Performance thresholds by stage (in seconds)
    STAGE_THRESHOLDS = {
        1: 5.0,   # Stage 1: Individual responses
        2: 5.0,   # Stage 2: Peer rankings
        3: 7.0    # Stage 3: Chairman synthesis
    }
    
    def __init__(self):
        """Initialize the performance monitor with empty metrics."""
        self.active_timers: Dict[str, Dict] = {}
        self.stage_metrics: List[Dict] = []
        self.model_timings: Dict[str, List[float]] = defaultdict(list)
    
    def start_stage(self, stage: int, context: Optional[Dict] = None) -> str:
        """
        Start timing a stage.
        
        Args:
            stage: Stage number (1, 2, or 3)
            context: Optional context dictionary with additional info
        
        Returns:
            str: Timer ID for use with end_stage()
        """
        timer_id = str(uuid.uuid4())
        
        self.active_timers[timer_id] = {
            "stage": stage,
            "start_time": time.time(),
            "context": context or {}
        }
        
        logger.debug(f"Stage {stage} started (timer: {timer_id[:8]})")
        
        return timer_id
    
    def end_stage(self, timer_id: str) -> float:
        """
        End timing a stage and record metrics.
        
        Args:
            timer_id: Timer ID returned by start_stage()
        
        Returns:
            float: Elapsed time in seconds
        
        Raises:
            KeyError: If timer_id is not found
        """
        if timer_id not in self.active_timers:
            logger.error(f"Timer {timer_id[:8]} not found")
            raise KeyError(f"Timer {timer_id} not found")
        
        timer = self.active_timers.pop(timer_id)
        end_time = time.time()
        duration = end_time - timer["start_time"]
        
        stage = timer["stage"]
        
        # Record stage metrics
        metric = {
            "stage": stage,
            "start_time": timer["start_time"],
            "end_time": end_time,
            "duration": duration,
            "context": timer["context"]
        }
        self.stage_metrics.append(metric)
        
        logger.info(f"Stage {stage} completed in {duration:.2f}s")
        
        # Check performance threshold
        self.check_performance_threshold(stage, duration)
        
        return duration
    
    def log_model_response(self, model: str, duration: float) -> None:
        """
        Log individual model response time.
        
        Args:
            model: Model identifier (e.g., "openai/gpt-4o-mini")
            duration: Response time in seconds
        """
        self.model_timings[model].append(duration)
        
        logger.debug(f"Model {model} responded in {duration:.2f}s")
    
    def check_performance_threshold(self, stage: int, duration: float) -> None:
        """
        Log warning if stage exceeds expected threshold.
        
        Args:
            stage: Stage number (1, 2, or 3)
            duration: Stage duration in seconds
        """
        threshold = self.STAGE_THRESHOLDS.get(stage)
        
        if threshold and duration > threshold:
            logger.warning(
                f"⚠️  Stage {stage} exceeded threshold: {duration:.2f}s > {threshold:.2f}s "
                f"(+{duration - threshold:.2f}s)"
            )
    
    def get_statistics(self) -> Dict:
        """
        Calculate aggregate statistics for all recorded metrics.
        
        Returns:
            dict: Statistics including:
                - stage_stats: Per-stage statistics (count, mean, p50, p90, p95, p99)
                - model_stats: Per-model statistics
                - total_queries: Total number of queries processed
        """
        stats = {
            "stage_stats": {},
            "model_stats": {},
            "total_queries": len(self.stage_metrics)
        }
        
        # Calculate per-stage statistics
        stage_durations = defaultdict(list)
        for metric in self.stage_metrics:
            stage_durations[metric["stage"]].append(metric["duration"])
        
        for stage, durations in stage_durations.items():
            if durations:
                stats["stage_stats"][stage] = self._calculate_percentiles(durations)
        
        # Calculate per-model statistics
        for model, durations in self.model_timings.items():
            if durations:
                stats["model_stats"][model] = self._calculate_percentiles(durations)
        
        return stats
    
    def _calculate_percentiles(self, values: List[float]) -> Dict:
        """
        Calculate percentile statistics for a list of values.
        
        Args:
            values: List of numeric values
        
        Returns:
            dict: Statistics with count, mean, p50, p90, p95, p99
        """
        if not values:
            return {
                "count": 0,
                "mean": 0.0,
                "p50": 0.0,
                "p90": 0.0,
                "p95": 0.0,
                "p99": 0.0
            }
        
        sorted_values = sorted(values)
        count = len(sorted_values)
        
        def percentile(p: float) -> float:
            """Calculate the p-th percentile."""
            index = int(count * p)
            if index >= count:
                index = count - 1
            return sorted_values[index]
        
        return {
            "count": count,
            "mean": sum(values) / count,
            "p50": percentile(0.50),
            "p90": percentile(0.90),
            "p95": percentile(0.95),
            "p99": percentile(0.99)
        }
    
    def get_summary(self) -> str:
        """
        Get a human-readable summary of performance statistics.
        
        Returns:
            str: Formatted summary string
        """
        stats = self.get_statistics()
        
        lines = [
            "Performance Summary:",
            f"  Total queries: {stats['total_queries']}"
        ]
        
        # Stage statistics
        if stats["stage_stats"]:
            lines.append("\n  Stage Statistics:")
            for stage in sorted(stats["stage_stats"].keys()):
                s = stats["stage_stats"][stage]
                lines.append(
                    f"    Stage {stage}: "
                    f"mean={s['mean']:.2f}s, "
                    f"p50={s['p50']:.2f}s, "
                    f"p90={s['p90']:.2f}s, "
                    f"p95={s['p95']:.2f}s "
                    f"({s['count']} samples)"
                )
        
        # Model statistics (top 5 by count)
        if stats["model_stats"]:
            lines.append("\n  Model Statistics (top 5):")
            sorted_models = sorted(
                stats["model_stats"].items(),
                key=lambda x: x[1]["count"],
                reverse=True
            )[:5]
            
            for model, s in sorted_models:
                model_name = model.split("/")[-1] if "/" in model else model
                lines.append(
                    f"    {model_name}: "
                    f"mean={s['mean']:.2f}s, "
                    f"p90={s['p90']:.2f}s "
                    f"({s['count']} calls)"
                )
        
        return "\n".join(lines)


# Global performance monitor instance
_performance_monitor = PerformanceMonitor()


def get_performance_monitor() -> PerformanceMonitor:
    """
    Get the global performance monitor instance.
    
    Returns:
        PerformanceMonitor: The global performance monitor
    """
    return _performance_monitor
