"""
Razorpay payment integration for subscription management.
"""
import os
import razorpay
import hmac
import hashlib
import logging
from datetime import datetime
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from models import Usage
from database import get_db

logger = logging.getLogger(__name__)

# Initialize Razorpay
RAZORPAY_KEY_ID = os.getenv('RAZORPAY_KEY_ID')
RAZORPAY_KEY_SECRET = os.getenv('RAZORPAY_KEY_SECRET')
RAZORPAY_WEBHOOK_SECRET = os.getenv('RAZORPAY_WEBHOOK_SECRET')

razorpay_client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

# Plan IDs from Razorpay Dashboard
RAZORPAY_PLAN_IDS = {
    'pro_monthly': os.getenv('RAZORPAY_PRO_MONTHLY_PLAN_ID'),
    'pro_yearly': os.getenv('RAZORPAY_PRO_YEARLY_PLAN_ID'),  # Optional
}


class PaymentService:
    """Service for handling Razorpay payments and subscriptions."""
    
    @staticmethod
    def create_subscription(
        user_id: str,
        user_email: str,
        plan_id: str,
        success_url: str,
        cancel_url: str
    ) -> Dict[str, Any]:
        """
        Create a Razorpay subscription for Pro plan.
        
        Args:
            user_id: User's unique identifier
            user_email: User's email address
            plan_id: Razorpay plan ID for the subscription
            success_url: URL to redirect after successful payment
            cancel_url: URL to redirect if payment is cancelled
            
        Returns:
            Dictionary with subscription details
        """
        try:
            # Create subscription
            subscription = razorpay_client.subscription.create({
                'plan_id': plan_id,
                'total_count': 12,  # 12 months for annual, adjust as needed
                'customer_notify': 1,
                'notes': {
                    'user_id': user_id,
                    'user_email': user_email,
                }
            })
            
            return {
                'success': True,
                'subscription_id': subscription['id'],
                'subscription': subscription
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    @staticmethod
    def cancel_subscription(subscription_id: str) -> Dict[str, Any]:
        """
        Cancel a Razorpay subscription.
        
        Args:
            subscription_id: Razorpay subscription ID
            
        Returns:
            Dictionary with cancellation status
        """
        try:
            subscription = razorpay_client.subscription.cancel(subscription_id)
            
            return {
                'success': True,
                'subscription': subscription
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    @staticmethod
    def fetch_subscription(subscription_id: str) -> Dict[str, Any]:
        """
        Fetch subscription details from Razorpay.
        
        Args:
            subscription_id: Razorpay subscription ID
            
        Returns:
            Dictionary with subscription details
        """
        try:
            subscription = razorpay_client.subscription.fetch(subscription_id)
            
            return {
                'success': True,
                'subscription': subscription
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    @staticmethod
    def verify_webhook_signature(payload: bytes, sig_header: str) -> bool:
        """
        Verify Razorpay webhook signature.
        
        Args:
            payload: Raw request body
            sig_header: Razorpay signature header (X-Razorpay-Signature)
            
        Returns:
            True if signature is valid, False otherwise
        """
        try:
            if not RAZORPAY_WEBHOOK_SECRET:
                logger.error("❌ RAZORPAY_WEBHOOK_SECRET not configured")
                return False
            
            if not sig_header:
                logger.error("❌ No signature header provided")
                return False
            
            # Generate expected signature
            expected_signature = hmac.new(
                RAZORPAY_WEBHOOK_SECRET.encode('utf-8'),
                payload,
                hashlib.sha256
            ).hexdigest()
            
            is_valid = hmac.compare_digest(expected_signature, sig_header)
            
            if not is_valid:
                logger.warning(f"⚠️  Signature mismatch - Expected: {expected_signature[:10]}..., Got: {sig_header[:10]}...")
            
            return is_valid
        except Exception as e:
            logger.error(f"❌ Error verifying webhook signature: {str(e)}")
            return False
    
    @staticmethod
    def handle_payment_authorized(payload: Dict[str, Any], db: Session) -> bool:
        """
        Handle successful payment authorization.
        
        Args:
            payload: Razorpay webhook payload
            db: Database session
            
        Returns:
            True if handled successfully
        """
        try:
            subscription_id = payload.get('payload', {}).get('subscription', {}).get('entity', {}).get('id')
            notes = payload.get('payload', {}).get('subscription', {}).get('entity', {}).get('notes', {})
            user_id = notes.get('user_id')
            
            logger.info(f"💳 Processing payment authorization - User: {user_id}, Subscription: {subscription_id}")
            
            if not user_id or not subscription_id:
                logger.error(f"❌ Missing required fields - user_id: {user_id}, subscription_id: {subscription_id}")
                return False
            
            # Update user to Pro tier
            usage = db.query(Usage).filter(Usage.user_id == user_id).first()
            if not usage:
                logger.warning(f"⚠️  User {user_id} not found, creating new usage record")
                usage = Usage(
                    user_id=user_id,
                    tier='pro',
                    daily_limit=100,
                    monthly_limit=3000,
                    razorpay_subscription_id=subscription_id,
                    subscription_status='active'
                )
                db.add(usage)
            else:
                logger.info(f"📝 Updating existing user {user_id} - Old tier: {usage.tier}")
                usage.tier = 'pro'
                usage.daily_limit = 100
                usage.monthly_limit = 3000
                usage.razorpay_subscription_id = subscription_id
                usage.subscription_status = 'active'
                usage.updated_at = datetime.utcnow()
            
            db.commit()
            logger.info(f"✅ Payment authorization processed successfully for user {user_id}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error handling payment authorization: {str(e)}")
            logger.error(f"User: {user_id if 'user_id' in locals() else 'unknown'}")
            db.rollback()
            return False
    
    @staticmethod
    def handle_subscription_updated(payload: Dict[str, Any], db: Session) -> bool:
        """
        Handle subscription update events.
        
        Args:
            payload: Razorpay webhook payload
            db: Database session
            
        Returns:
            True if handled successfully
        """
        try:
            subscription_entity = payload.get('payload', {}).get('subscription', {}).get('entity', {})
            subscription_id = subscription_entity.get('id')
            status = subscription_entity.get('status')
            notes = subscription_entity.get('notes', {})
            user_id = notes.get('user_id')
            
            logger.info(f"🔄 Processing subscription update - Subscription: {subscription_id}, Status: {status}")
            
            if not user_id:
                logger.warning(f"⚠️  user_id not in notes, looking up by subscription_id: {subscription_id}")
                # Try to find user by subscription_id
                usage = db.query(Usage).filter(Usage.razorpay_subscription_id == subscription_id).first()
                if not usage:
                    logger.error(f"❌ User not found for subscription_id: {subscription_id}")
                    return False
                user_id = usage.user_id
                logger.info(f"✓ Found user: {user_id}")
            else:
                usage = db.query(Usage).filter(Usage.user_id == user_id).first()
                if not usage:
                    logger.error(f"❌ User not found: {user_id}")
                    return False
            
            old_status = usage.subscription_status
            old_tier = usage.tier
            
            usage.subscription_status = status
            
            # Update tier based on status
            if status == 'active':
                usage.tier = 'pro'
                usage.daily_limit = 100
                usage.monthly_limit = 3000
                logger.info(f"📈 Upgrading user {user_id} to Pro tier")
            elif status in ['cancelled', 'completed', 'expired', 'halted']:
                usage.tier = 'free'
                usage.daily_limit = 10
                usage.monthly_limit = 300
                logger.info(f"📉 Downgrading user {user_id} to Free tier (status: {status})")
            else:
                logger.warning(f"⚠️  Unknown status: {status}, keeping current tier")
            
            usage.updated_at = datetime.utcnow()
            db.commit()
            
            logger.info(f"✅ Subscription updated - User: {user_id}, "
                       f"Status: {old_status} → {status}, Tier: {old_tier} → {usage.tier}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error handling subscription update: {str(e)}")
            logger.error(f"Subscription: {subscription_id if 'subscription_id' in locals() else 'unknown'}")
            db.rollback()
            return False
    
    @staticmethod
    def handle_subscription_cancelled(payload: Dict[str, Any], db: Session) -> bool:
        """
        Handle subscription cancellation.
        
        Args:
            payload: Razorpay webhook payload
            db: Database session
            
        Returns:
            True if handled successfully
        """
        try:
            subscription_entity = payload.get('payload', {}).get('subscription', {}).get('entity', {})
            subscription_id = subscription_entity.get('id')
            notes = subscription_entity.get('notes', {})
            user_id = notes.get('user_id')
            
            logger.info(f"🚫 Processing subscription cancellation - Subscription: {subscription_id}")
            
            if not user_id:
                logger.warning(f"⚠️  user_id not in notes, looking up by subscription_id: {subscription_id}")
                # Try to find user by subscription_id
                usage = db.query(Usage).filter(Usage.razorpay_subscription_id == subscription_id).first()
                if not usage:
                    logger.error(f"❌ User not found for subscription_id: {subscription_id}")
                    return False
                user_id = usage.user_id
                logger.info(f"✓ Found user: {user_id}")
            else:
                usage = db.query(Usage).filter(Usage.user_id == user_id).first()
                if not usage:
                    logger.error(f"❌ User not found: {user_id}")
                    return False
            
            old_tier = usage.tier
            old_subscription_id = usage.razorpay_subscription_id
            
            usage.tier = 'free'
            usage.daily_limit = 10
            usage.monthly_limit = 300
            usage.subscription_status = 'cancelled'
            usage.razorpay_subscription_id = None
            usage.updated_at = datetime.utcnow()
            db.commit()
            
            logger.info(f"✅ Subscription cancelled - User: {user_id}, "
                       f"Tier: {old_tier} → free, Subscription ID cleared: {old_subscription_id}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error handling subscription cancellation: {str(e)}")
            logger.error(f"Subscription: {subscription_id if 'subscription_id' in locals() else 'unknown'}")
            db.rollback()
            return False
    
    @staticmethod
    def get_subscription_info(user_id: str, db: Session) -> Optional[Dict[str, Any]]:
        """
        Get subscription information for a user.
        
        Args:
            user_id: User's unique identifier
            db: Database session
            
        Returns:
            Dictionary with subscription details or None
        """
        usage = db.query(Usage).filter(Usage.user_id == user_id).first()
        if not usage:
            return None
        
        result = {
            'tier': usage.tier,
            'status': getattr(usage, 'subscription_status', None),
            'subscription_id': getattr(usage, 'razorpay_subscription_id', None),
        }
        
        # Fetch live subscription data from Razorpay if available
        if result['subscription_id']:
            try:
                subscription = razorpay_client.subscription.fetch(result['subscription_id'])
                result['current_period_end'] = subscription.get('current_end')
                result['next_billing_at'] = subscription.get('charge_at')
                result['plan_id'] = subscription.get('plan_id')
            except Exception:
                pass
        
        return result
    
    @staticmethod
    def verify_and_sync_subscription(user_id: str, db: Session) -> Dict[str, Any]:
        """
        Verify subscription status with Razorpay and sync with local database.
        
        This method fetches the subscription from Razorpay API and compares it with
        the local database. If there's a mismatch, it updates the local database
        and logs the discrepancy.
        
        Args:
            user_id: User's unique identifier
            db: Database session
            
        Returns:
            Dictionary with verification results and current status
        """
        try:
            logger.info(f"🔍 Verifying subscription status for user: {user_id}")
            
            # Get user's usage record
            usage = db.query(Usage).filter(Usage.user_id == user_id).first()
            if not usage:
                logger.warning(f"⚠️  User {user_id} not found in database")
                return {
                    'success': False,
                    'error': 'User not found',
                    'tier': 'free',
                    'status': None
                }
            
            # Check if user has a subscription ID
            subscription_id = usage.razorpay_subscription_id
            if not subscription_id:
                logger.info(f"ℹ️  User {user_id} has no subscription ID - returning cached data")
                return {
                    'success': True,
                    'synced': False,
                    'tier': usage.tier,
                    'status': usage.subscription_status,
                    'message': 'No subscription ID found'
                }
            
            # Store current state for comparison
            old_tier = usage.tier
            old_status = usage.subscription_status
            
            # Fetch subscription from Razorpay API
            try:
                logger.info(f"📡 Fetching subscription {subscription_id} from Razorpay API")
                subscription = razorpay_client.subscription.fetch(subscription_id)
                razorpay_status = subscription.get('status')
                
                logger.info(f"✓ Razorpay API response - Status: {razorpay_status}")
                
                # Check for mismatch
                mismatch_detected = False
                if old_status != razorpay_status:
                    logger.warning(f"⚠️  MISMATCH DETECTED - User: {user_id}")
                    logger.warning(f"   Local status: {old_status}, Razorpay status: {razorpay_status}")
                    mismatch_detected = True
                
                # Update database if status changed
                if razorpay_status != old_status:
                    usage.subscription_status = razorpay_status
                    
                    # Update tier based on status
                    if razorpay_status == 'active':
                        usage.tier = 'pro'
                        usage.daily_limit = 100
                        usage.monthly_limit = 3000
                        logger.info(f"📈 Syncing user {user_id} to Pro tier")
                    elif razorpay_status in ['cancelled', 'completed', 'expired', 'halted']:
                        usage.tier = 'free'
                        usage.daily_limit = 10
                        usage.monthly_limit = 300
                        logger.info(f"📉 Syncing user {user_id} to Free tier (status: {razorpay_status})")
                    
                    usage.updated_at = datetime.utcnow()
                    db.commit()
                    
                    logger.info(f"✅ Subscription synced - User: {user_id}, "
                               f"Status: {old_status} → {razorpay_status}, "
                               f"Tier: {old_tier} → {usage.tier}")
                    
                    return {
                        'success': True,
                        'synced': True,
                        'mismatch_detected': mismatch_detected,
                        'tier': usage.tier,
                        'status': usage.subscription_status,
                        'old_tier': old_tier,
                        'old_status': old_status,
                        'message': 'Subscription status updated from Razorpay'
                    }
                else:
                    logger.info(f"✓ Subscription status matches - No sync needed")
                    return {
                        'success': True,
                        'synced': False,
                        'tier': usage.tier,
                        'status': usage.subscription_status,
                        'message': 'Subscription status already up to date'
                    }
                    
            except razorpay.errors.BadRequestError as e:
                # Subscription not found in Razorpay
                logger.error(f"❌ Subscription {subscription_id} not found in Razorpay: {str(e)}")
                logger.warning(f"⚠️  Marking subscription as invalid for user {user_id}")
                
                # Downgrade to free tier
                usage.tier = 'free'
                usage.daily_limit = 10
                usage.monthly_limit = 300
                usage.subscription_status = 'invalid'
                usage.updated_at = datetime.utcnow()
                db.commit()
                
                return {
                    'success': True,
                    'synced': True,
                    'tier': 'free',
                    'status': 'invalid',
                    'message': 'Subscription not found in Razorpay - downgraded to free tier'
                }
                
            except Exception as api_error:
                # API failure - use cached data
                logger.error(f"❌ Razorpay API error: {str(api_error)}")
                logger.info(f"ℹ️  Using cached database value for user {user_id}")
                
                return {
                    'success': True,
                    'synced': False,
                    'tier': usage.tier,
                    'status': usage.subscription_status,
                    'api_error': str(api_error),
                    'message': 'API unavailable - using cached data'
                }
                
        except Exception as e:
            logger.error(f"❌ Error verifying subscription: {str(e)}")
            db.rollback()
            return {
                'success': False,
                'error': str(e),
                'message': 'Verification failed'
            }
