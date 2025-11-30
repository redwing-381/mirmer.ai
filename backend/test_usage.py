"""
Property-based tests for usage tracking system.

Feature: ui-improvements, Property 5: Usage increment consistency
Validates: Requirements 6.1, 6.2, 6.4
"""
import pytest
from hypothesis import given, strategies as st, settings
from datetime import date, datetime
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Mock the database before importing usage modules
mock_session = MagicMock()
mock_session_local = MagicMock(return_value=mock_session)

with patch('database.SessionLocal', mock_session_local):
    import usage_postgres


class TestUsageIncrement:
    """
    Property-based tests for usage increment functionality.
    
    **Feature: ui-improvements, Property 5: Usage increment consistency**
    **Validates: Requirements 6.1, 6.2, 6.4**
    """
    
    @given(
        user_id=st.text(min_size=1, max_size=50, alphabet=st.characters(blacklist_characters=['\x00'])),
        initial_daily=st.integers(min_value=0, max_value=100),
        initial_monthly=st.integers(min_value=0, max_value=1000),
        initial_total=st.integers(min_value=0, max_value=10000)
    )
    @settings(max_examples=100)
    def test_increment_increases_all_counters(self, user_id, initial_daily, initial_monthly, initial_total):
        """
        Property: For any user and any initial usage state, incrementing usage
        should increase daily_used, monthly_used, and total_queries by exactly 1.
        
        This tests that the increment operation is atomic and consistent.
        """
        # Create mock usage object
        mock_usage = Mock()
        mock_usage.user_id = user_id
        mock_usage.tier = 'free'
        mock_usage.daily_used = initial_daily
        mock_usage.monthly_used = initial_monthly
        mock_usage.total_queries = initial_total
        mock_usage.daily_limit = 10
        mock_usage.monthly_limit = 100
        mock_usage.last_reset_daily = date.today()
        mock_usage.last_reset_monthly = date.today()
        mock_usage.updated_at = datetime.utcnow()
        
        # Mock session and query
        mock_session_instance = MagicMock()
        mock_session_instance.__enter__ = Mock(return_value=mock_session_instance)
        mock_session_instance.__exit__ = Mock(return_value=False)
        mock_session_instance.query.return_value.filter.return_value.first.return_value = mock_usage
        
        with patch('usage_postgres.SessionLocal', return_value=mock_session_instance):
            # Call increment_usage
            result = usage_postgres.increment_usage(user_id)
            
            # Verify result
            assert result is True, "Increment should return True on success"
            
            # Verify all counters increased by 1
            assert mock_usage.daily_used == initial_daily + 1, "Daily counter should increment by 1"
            assert mock_usage.monthly_used == initial_monthly + 1, "Monthly counter should increment by 1"
            assert mock_usage.total_queries == initial_total + 1, "Total counter should increment by 1"
            
            # Verify commit was called
            mock_session_instance.commit.assert_called()
    
    @given(
        user_id=st.text(min_size=1, max_size=50, alphabet=st.characters(blacklist_characters=['\x00'])),
        num_increments=st.integers(min_value=1, max_value=20)
    )
    @settings(max_examples=100)
    def test_multiple_increments_are_cumulative(self, user_id, num_increments):
        """
        Property: For any user, performing N increments should result in
        counters increasing by exactly N.
        
        This tests that multiple increments are cumulative and don't interfere
        with each other.
        """
        # Create mock usage object
        mock_usage = Mock()
        mock_usage.user_id = user_id
        mock_usage.tier = 'free'
        mock_usage.daily_used = 0
        mock_usage.monthly_used = 0
        mock_usage.total_queries = 0
        mock_usage.daily_limit = 10
        mock_usage.monthly_limit = 100
        mock_usage.last_reset_daily = date.today()
        mock_usage.last_reset_monthly = date.today()
        mock_usage.updated_at = datetime.utcnow()
        
        # Mock session
        mock_session_instance = MagicMock()
        mock_session_instance.__enter__ = Mock(return_value=mock_session_instance)
        mock_session_instance.__exit__ = Mock(return_value=False)
        mock_session_instance.query.return_value.filter.return_value.first.return_value = mock_usage
        
        with patch('usage_postgres.SessionLocal', return_value=mock_session_instance):
            # Perform multiple increments
            for _ in range(num_increments):
                result = usage_postgres.increment_usage(user_id)
                assert result is True
            
            # Verify counters match number of increments
            assert mock_usage.daily_used == num_increments
            assert mock_usage.monthly_used == num_increments
            assert mock_usage.total_queries == num_increments
    
    @given(
        user_id=st.text(min_size=1, max_size=50, alphabet=st.characters(blacklist_characters=['\x00']))
    )
    @settings(max_examples=100)
    def test_increment_creates_new_user_if_not_exists(self, user_id):
        """
        Property: For any user_id that doesn't exist in the database,
        increment_usage should create a new usage record with initial values
        and then increment.
        
        This tests the auto-creation behavior for new users.
        """
        # Mock session with no existing user
        mock_session_instance = MagicMock()
        mock_session_instance.__enter__ = Mock(return_value=mock_session_instance)
        mock_session_instance.__exit__ = Mock(return_value=False)
        mock_session_instance.query.return_value.filter.return_value.first.return_value = None
        
        # Track the usage object that gets added
        added_usage = None
        def capture_add(usage):
            nonlocal added_usage
            added_usage = usage
        
        mock_session_instance.add = Mock(side_effect=capture_add)
        
        with patch('usage_postgres.SessionLocal', return_value=mock_session_instance):
            with patch('usage_postgres.Usage') as mock_usage_class:
                # Create a mock instance that will be returned by Usage()
                mock_usage_instance = Mock()
                mock_usage_instance.user_id = user_id
                mock_usage_instance.tier = 'free'
                mock_usage_instance.daily_used = 0
                mock_usage_instance.monthly_used = 0
                mock_usage_instance.total_queries = 0
                mock_usage_instance.daily_limit = 10
                mock_usage_instance.monthly_limit = 100
                mock_usage_instance.last_reset_daily = date.today()
                mock_usage_instance.last_reset_monthly = date.today()
                
                mock_usage_class.return_value = mock_usage_instance
                
                # Call increment
                result = usage_postgres.increment_usage(user_id)
                
                # Verify new user was created
                assert result is True
                mock_usage_class.assert_called_once()
                
                # Verify counters were incremented from 0
                assert mock_usage_instance.daily_used == 1
                assert mock_usage_instance.monthly_used == 1
                assert mock_usage_instance.total_queries == 1
    
    @given(
        user_id=st.text(min_size=1, max_size=50, alphabet=st.characters(blacklist_characters=['\x00'])),
        tier=st.sampled_from(['free', 'pro', 'enterprise'])
    )
    @settings(max_examples=100)
    def test_increment_works_for_all_tiers(self, user_id, tier):
        """
        Property: For any user tier (free, pro, enterprise), increment_usage
        should work correctly and increase counters.
        
        This tests that the increment logic is tier-agnostic.
        """
        # Create mock usage object with specified tier
        mock_usage = Mock()
        mock_usage.user_id = user_id
        mock_usage.tier = tier
        mock_usage.daily_used = 5
        mock_usage.monthly_used = 50
        mock_usage.total_queries = 100
        mock_usage.daily_limit = 10 if tier == 'free' else 999999
        mock_usage.monthly_limit = 100 if tier == 'free' else 999999
        mock_usage.last_reset_daily = date.today()
        mock_usage.last_reset_monthly = date.today()
        mock_usage.updated_at = datetime.utcnow()
        
        # Mock session
        mock_session_instance = MagicMock()
        mock_session_instance.__enter__ = Mock(return_value=mock_session_instance)
        mock_session_instance.__exit__ = Mock(return_value=False)
        mock_session_instance.query.return_value.filter.return_value.first.return_value = mock_usage
        
        with patch('usage_postgres.SessionLocal', return_value=mock_session_instance):
            # Call increment
            result = usage_postgres.increment_usage(user_id)
            
            # Verify increment worked regardless of tier
            assert result is True
            assert mock_usage.daily_used == 6
            assert mock_usage.monthly_used == 51
            assert mock_usage.total_queries == 101


class TestUsageStats:
    """
    Property-based tests for usage stats retrieval.
    
    **Feature: ui-improvements, Property 5: Usage increment consistency**
    **Validates: Requirements 6.2**
    """
    
    @given(
        user_id=st.text(min_size=1, max_size=50, alphabet=st.characters(blacklist_characters=['\x00'])),
        daily_used=st.integers(min_value=0, max_value=100),
        monthly_used=st.integers(min_value=0, max_value=1000),
        total_queries=st.integers(min_value=0, max_value=10000),
        tier=st.sampled_from(['free', 'pro', 'enterprise'])
    )
    @settings(max_examples=100)
    def test_get_stats_returns_correct_field_names(self, user_id, daily_used, monthly_used, total_queries, tier):
        """
        Property: For any user with any usage values, get_usage_stats should
        return a dictionary with both 'daily_queries_used' and 'daily_used' fields
        (for frontend compatibility).
        
        This tests that the API returns the correct field names expected by the frontend.
        """
        # Create mock usage object
        mock_usage = Mock()
        mock_usage.user_id = user_id
        mock_usage.tier = tier
        mock_usage.daily_used = daily_used
        mock_usage.monthly_used = monthly_used
        mock_usage.total_queries = total_queries
        mock_usage.daily_limit = 10 if tier == 'free' else 999999
        mock_usage.monthly_limit = 100 if tier == 'free' else 999999
        mock_usage.last_reset_daily = date.today()
        mock_usage.last_reset_monthly = date.today()
        
        # Mock session
        mock_session_instance = MagicMock()
        mock_session_instance.__enter__ = Mock(return_value=mock_session_instance)
        mock_session_instance.__exit__ = Mock(return_value=False)
        mock_session_instance.query.return_value.filter.return_value.first.return_value = mock_usage
        
        with patch('usage_postgres.SessionLocal', return_value=mock_session_instance):
            # Get stats
            stats = usage_postgres.get_usage_stats(user_id)
            
            # Verify required fields exist
            assert 'daily_queries_used' in stats, "Stats must include 'daily_queries_used' for frontend"
            assert 'daily_used' in stats, "Stats must include 'daily_used' for backward compatibility"
            assert 'monthly_queries_used' in stats, "Stats must include 'monthly_queries_used' for frontend"
            assert 'monthly_used' in stats, "Stats must include 'monthly_used' for backward compatibility"
            
            # Verify values match
            assert stats['daily_queries_used'] == daily_used
            assert stats['daily_used'] == daily_used
            assert stats['monthly_queries_used'] == monthly_used
            assert stats['monthly_used'] == monthly_used
            assert stats['total_queries'] == total_queries


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
