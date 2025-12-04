"""
Quick performance test for the optimized council system.
"""
import asyncio
import time
from council import stage1_collect_responses, stage2_collect_rankings, stage3_synthesize_final
from performance import get_performance_monitor

async def test_council_performance():
    """Test the full 3-stage council process and measure performance."""
    
    print("=" * 60)
    print("🧪 Testing Mirmer AI Performance Optimizations")
    print("=" * 60)
    print()
    
    # Test query
    test_query = "What are the key benefits of using AI in software development?"
    
    print(f"📝 Test Query: {test_query}")
    print()
    print("⏱️  Starting 3-stage council process...")
    print()
    
    # Track total time
    total_start = time.time()
    
    try:
        # Stage 1: Collect responses
        print("🔄 Stage 1: Collecting responses from council models...")
        stage1_start = time.time()
        stage1_results = await stage1_collect_responses(test_query)
        stage1_duration = time.time() - stage1_start
        print(f"   ✓ Stage 1 completed in {stage1_duration:.2f}s")
        print(f"   ✓ Received {len(stage1_results)} responses")
        print()
        
        # Stage 2: Collect rankings
        print("🔄 Stage 2: Collecting peer rankings...")
        stage2_start = time.time()
        stage2_results, label_to_model = await stage2_collect_rankings(test_query, stage1_results)
        stage2_duration = time.time() - stage2_start
        print(f"   ✓ Stage 2 completed in {stage2_duration:.2f}s")
        print(f"   ✓ Received {len(stage2_results)} rankings")
        print()
        
        # Stage 3: Chairman synthesis
        print("🔄 Stage 3: Chairman synthesizing final answer...")
        stage3_start = time.time()
        stage3_result = await stage3_synthesize_final(test_query, stage1_results, stage2_results)
        stage3_duration = time.time() - stage3_start
        print(f"   ✓ Stage 3 completed in {stage3_duration:.2f}s")
        print()
        
        # Total time
        total_duration = time.time() - total_start
        
        print("=" * 60)
        print("📊 Performance Summary")
        print("=" * 60)
        print(f"Stage 1 Duration:  {stage1_duration:>6.2f}s")
        print(f"Stage 2 Duration:  {stage2_duration:>6.2f}s")
        print(f"Stage 3 Duration:  {stage3_duration:>6.2f}s")
        print("-" * 60)
        print(f"Total Duration:    {total_duration:>6.2f}s")
        print("=" * 60)
        print()
        
        # Get detailed performance statistics
        perf_monitor = get_performance_monitor()
        stats = perf_monitor.get_statistics()
        
        print("📈 Detailed Performance Metrics")
        print("=" * 60)
        
        # Stage statistics
        if stats["stage_stats"]:
            print("\n🎯 Stage Statistics:")
            for stage in sorted(stats["stage_stats"].keys()):
                s = stats["stage_stats"][stage]
                print(f"   Stage {stage}:")
                print(f"      Mean:  {s['mean']:.2f}s")
                print(f"      p50:   {s['p50']:.2f}s")
                print(f"      p90:   {s['p90']:.2f}s")
        
        # Model statistics
        if stats["model_stats"]:
            print("\n🤖 Model Response Times:")
            sorted_models = sorted(
                stats["model_stats"].items(),
                key=lambda x: x[1]["mean"]
            )
            for model, s in sorted_models:
                model_name = model.split("/")[-1] if "/" in model else model
                print(f"   {model_name:25s}: {s['mean']:.2f}s (calls: {s['count']})")
        
        print()
        print("=" * 60)
        
        # Performance assessment
        if total_duration < 15:
            print("🎉 EXCELLENT! Under 15 seconds target!")
        elif total_duration < 20:
            print("✅ GOOD! Within acceptable range (15-20s)")
        elif total_duration < 25:
            print("⚠️  ACCEPTABLE but could be improved (20-25s)")
        else:
            print("❌ SLOW - Consider using 'speed' tier")
        
        print("=" * 60)
        print()
        
        # Show first 200 chars of final answer
        if stage3_result and stage3_result.get("response"):
            print("💬 Final Answer Preview:")
            print("-" * 60)
            answer = stage3_result["response"]
            preview = answer[:200] + "..." if len(answer) > 200 else answer
            print(preview)
            print("-" * 60)
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error during test: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_council_performance())
    exit(0 if success else 1)
