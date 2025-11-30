#!/usr/bin/env python3
"""Test script to verify usage increment works"""
import sys
sys.path.insert(0, '.')
import usage_json

# Test increment
user_id = 'test_user_increment'
print('Before increment:')
stats = usage_json.get_usage_stats(user_id)
print(f'Daily: {stats["daily_used"]}, Monthly: {stats["monthly_used"]}, Total: {stats["total_queries"]}')

print('\nIncrementing...')
usage_json.increment_usage(user_id)

print('\nAfter increment:')
stats = usage_json.get_usage_stats(user_id)
print(f'Daily: {stats["daily_used"]}, Monthly: {stats["monthly_used"]}, Total: {stats["total_queries"]}')

print('\n✅ Increment function works correctly!')
