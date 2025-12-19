"""
User Database Module for AUREA PRIME ELITE
Handles all user-related database operations
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, List, Any


class UserDB:
    """
    UserDB class for managing user data in AUREA PRIME ELITE.
    Provides methods for user creation, retrieval, and management.
    """

    def __init__(self, db_connection):
        """
        Initialize UserDB with a database connection.
        
        Args:
            db_connection: Database connection object
        """
        self.db = db_connection
        self.collection = self.db.get_collection('users')

    def create_user(self, user_id: str, username: str, tier: str = 'free', **kwargs) -> Dict[str, Any]:
        """
        Create a new user in the database.
        
        Args:
            user_id: Unique identifier for the user
            username: User's display name
            tier: Subscription tier (default: 'free')
            **kwargs: Additional user attributes
            
        Returns:
            Dict containing the created user data
        """
        user_data = {
            'user_id': user_id,
            'username': username,
            'tier': tier,
            'mt5_id': kwargs.get('mt5_id'),
            'settings': kwargs.get('settings', {}),
            'daily_signals_count': 0,
            'daily_signals_reset': datetime.utcnow().date().isoformat(),
            'subscription_start': datetime.utcnow().isoformat(),
            'subscription_end': kwargs.get('subscription_end'),
            'created_at': datetime.utcnow().isoformat(),
            'updated_at': datetime.utcnow().isoformat()
        }
        self.collection.insert_one(user_data)
        return user_data

    def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a user by their ID.
        
        Args:
            user_id: The unique identifier of the user
            
        Returns:
            Dict containing user data or None if not found
        """
        return self.collection.find_one({'user_id': user_id})

    def update_tier(self, user_id: str, new_tier: str, duration_days: int = 30) -> bool:
        """
        Update a user's subscription tier.
        
        Args:
            user_id: The unique identifier of the user
            new_tier: The new subscription tier
            duration_days: Duration of the subscription in days (default: 30)
            
        Returns:
            bool indicating success or failure
        """
        subscription_end = datetime.utcnow() + timedelta(days=duration_days)
        result = self.collection.update_one(
            {'user_id': user_id},
            {
                '$set': {
                    'tier': new_tier,
                    'subscription_start': datetime.utcnow().isoformat(),
                    'subscription_end': subscription_end.isoformat(),
                    'updated_at': datetime.utcnow().isoformat()
                }
            }
        )
        return result.modified_count > 0

    def update_mt5_id(self, user_id: str, mt5_id: str) -> bool:
        """
        Update a user's MT5 trading account ID.
        
        Args:
            user_id: The unique identifier of the user
            mt5_id: The MetaTrader 5 account ID
            
        Returns:
            bool indicating success or failure
        """
        result = self.collection.update_one(
            {'user_id': user_id},
            {
                '$set': {
                    'mt5_id': mt5_id,
                    'updated_at': datetime.utcnow().isoformat()
                }
            }
        )
        return result.modified_count > 0

    def update_settings(self, user_id: str, settings: Dict[str, Any]) -> bool:
        """
        Update a user's settings.
        
        Args:
            user_id: The unique identifier of the user
            settings: Dictionary containing user settings
            
        Returns:
            bool indicating success or failure
        """
        result = self.collection.update_one(
            {'user_id': user_id},
            {
                '$set': {
                    'settings': settings,
                    'updated_at': datetime.utcnow().isoformat()
                }
            }
        )
        return result.modified_count > 0

    def increment_daily_signals(self, user_id: str) -> Dict[str, Any]:
        """
        Increment the daily signals count for a user.
        Resets the count if it's a new day.
        
        Args:
            user_id: The unique identifier of the user
            
        Returns:
            Dict with updated count and remaining signals
        """
        user = self.get_user(user_id)
        if not user:
            return {'success': False, 'error': 'User not found'}

        today = datetime.utcnow().date().isoformat()
        
        # Reset count if it's a new day
        if user.get('daily_signals_reset') != today:
            self.collection.update_one(
                {'user_id': user_id},
                {
                    '$set': {
                        'daily_signals_count': 1,
                        'daily_signals_reset': today,
                        'updated_at': datetime.utcnow().isoformat()
                    }
                }
            )
            return {'success': True, 'count': 1}
        else:
            result = self.collection.update_one(
                {'user_id': user_id},
                {
                    '$inc': {'daily_signals_count': 1},
                    '$set': {'updated_at': datetime.utcnow().isoformat()}
                }
            )
            new_count = user.get('daily_signals_count', 0) + 1
            return {'success': True, 'count': new_count}

    def check_expired_subscriptions(self) -> List[Dict[str, Any]]:
        """
        Check for users with expired subscriptions.
        
        Returns:
            List of users with expired subscriptions
        """
        now = datetime.utcnow().isoformat()
        expired_users = list(self.collection.find({
            'tier': {'$ne': 'free'},
            'subscription_end': {'$lt': now}
        }))
        return expired_users

    def downgrade_to_free(self, user_id: str) -> bool:
        """
        Downgrade a user's subscription to the free tier.
        
        Args:
            user_id: The unique identifier of the user
            
        Returns:
            bool indicating success or failure
        """
        result = self.collection.update_one(
            {'user_id': user_id},
            {
                '$set': {
                    'tier': 'free',
                    'subscription_end': None,
                    'updated_at': datetime.utcnow().isoformat()
                }
            }
        )
        return result.modified_count > 0

    def get_all_users_by_tier(self, tier: str) -> List[Dict[str, Any]]:
        """
        Retrieve all users with a specific subscription tier.
        
        Args:
            tier: The subscription tier to filter by
            
        Returns:
            List of users with the specified tier
        """
        return list(self.collection.find({'tier': tier}))

    def get_user_stats(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Get comprehensive statistics for a user.
        
        Args:
            user_id: The unique identifier of the user
            
        Returns:
            Dict containing user statistics or None if not found
        """
        user = self.get_user(user_id)
        if not user:
            return None

        # Calculate subscription status
        subscription_active = False
        days_remaining = 0
        
        if user.get('tier') != 'free' and user.get('subscription_end'):
            end_date = datetime.fromisoformat(user['subscription_end'])
            now = datetime.utcnow()
            subscription_active = end_date > now
            if subscription_active:
                days_remaining = (end_date - now).days

        return {
            'user_id': user['user_id'],
            'username': user['username'],
            'tier': user['tier'],
            'mt5_connected': user.get('mt5_id') is not None,
            'subscription_active': subscription_active,
            'days_remaining': days_remaining,
            'daily_signals_used': user.get('daily_signals_count', 0),
            'member_since': user.get('created_at'),
            'last_updated': user.get('updated_at')
        }
