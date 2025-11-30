"""
Razorpay payment integration for subscription management.
"""
import os
import razorpay
import hmac
import hashlib
from datetime import datetime
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from models import Usage
from database import get_db

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
            # Generate expected signature
            expected_signature = hmac.new(
                RAZORPAY_WEBHOOK_SECRET.encode('utf-8'),
                payload,
                hashlib.sha256
            ).hexdigest()
            
            return hmac.compare_digest(expected_signature, sig_header)
        except Exception:
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
            
            if not user_id or not subscription_id:
                return False
            
            # Update user to Pro tier
            usage = db.query(Usage).filter(Usage.user_id == user_id).first()
            if usage:
                usage.tier = 'pro'
                usage.daily_limit = 100
                usage.monthly_limit = 3000
                usage.razorpay_subscription_id = subscription_id
                usage.subscription_status = 'active'
                usage.updated_at = datetime.utcnow()
                db.commit()
                return True
            
            return False
        except Exception:
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
            
            if not user_id:
                # Try to find user by subscription_id
                usage = db.query(Usage).filter(Usage.razorpay_subscription_id == subscription_id).first()
                if not usage:
                    return False
            else:
                usage = db.query(Usage).filter(Usage.user_id == user_id).first()
                if not usage:
                    return False
            
            usage.subscription_status = status
            
            # Update tier based on status
            if status == 'active':
                usage.tier = 'pro'
                usage.daily_limit = 100
                usage.monthly_limit = 3000
            elif status in ['cancelled', 'completed', 'expired', 'halted']:
                usage.tier = 'free'
                usage.daily_limit = 10
                usage.monthly_limit = 300
            
            usage.updated_at = datetime.utcnow()
            db.commit()
            return True
        except Exception:
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
            
            if not user_id:
                # Try to find user by subscription_id
                usage = db.query(Usage).filter(Usage.razorpay_subscription_id == subscription_id).first()
                if not usage:
                    return False
            else:
                usage = db.query(Usage).filter(Usage.user_id == user_id).first()
                if not usage:
                    return False
            
            usage.tier = 'free'
            usage.daily_limit = 10
            usage.monthly_limit = 300
            usage.subscription_status = 'cancelled'
            usage.razorpay_subscription_id = None
            usage.updated_at = datetime.utcnow()
            db.commit()
            return True
        except Exception:
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
