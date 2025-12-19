"""
Token Database Module for AUREA PRIME ELITE
Handles EA token management for SUPER/SUPREME users
"""

import secrets
import string
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Any


class TokenDB:
    """TokenDB class for managing EA tokens in AUREA PRIME ELITE."""

    def __init__(self, db_connection):
        self.db = db_connection
        self.collection = self.db.get_collection('tokens')

    @staticmethod
    def generate_token(length: int = 8) -> str:
        characters = string.ascii_uppercase + string.digits
        return ''.join(secrets.choice(characters) for _ in range(length))

    def create_token(self, user_id: str, mt5_id: str, tier: str, 
                     duration_days: int = 30) -> Dict[str, Any]:
        existing = self.get_token_by_user(user_id)
        if existing and existing.get('is_active'):
            self.deactivate_token(existing['token'])

        token = self.generate_token()
        expired_at = datetime.utcnow() + timedelta(days=duration_days)
        
        token_data = {
            'token': token,
            'user_id': user_id,
            'mt5_id': mt5_id,
            'tier': tier,
            'is_active': True,
            'expired_at': expired_at.isoformat(),
            'created_at': datetime.utcnow().isoformat(),
            'last_used': None,
            'usage_count': 0
        }
        
        self.collection.insert_one(token_data)
        return token_data

    def validate_token(self, token: str, mt5_id: str) -> Dict[str, Any]:
        token_data = self.collection.find_one({'token': token})
        
        if not token_data:
            return {'valid': False, 'error': 'Token not found'}
        
        if not token_data.get('is_active'):
            return {'valid': False, 'error': 'Token is deactivated'}
        
        if token_data.get('mt5_id') != mt5_id:
            return {'valid': False, 'error': 'MT5 ID mismatch'}
        
        expired_at = datetime.fromisoformat(token_data['expired_at'])
        if datetime.utcnow() > expired_at:
            self.deactivate_token(token)
            return {'valid': False, 'error': 'Token expired'}
        
        self.collection.update_one(
            {'token': token},
            {
                '$set': {'last_used': datetime.utcnow().isoformat()},
                '$inc': {'usage_count': 1}
            }
        )
        
        return {
            'valid': True,
            'user_id': token_data['user_id'],
            'tier': token_data['tier'],
            'expired_at': token_data['expired_at']
        }

    def get_token_by_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        return self.collection.find_one({'user_id': user_id, 'is_active': True})

    def get_token_by_mt5(self, mt5_id: str) -> Optional[Dict[str, Any]]:
        return self.collection.find_one({'mt5_id': mt5_id, 'is_active': True})

    def deactivate_token(self, token: str) -> bool:
        result = self.collection.update_one({'token': token}, {'$set': {'is_active': False}})
        return result.modified_count > 0

    def deactivate_user_tokens(self, user_id: str) -> int:
        result = self.collection.update_many(
            {'user_id': user_id, 'is_active': True},
            {'$set': {'is_active': False}}
        )
        return result.modified_count

    def extend_token(self, token: str, additional_days: int) -> bool:
        token_data = self.collection.find_one({'token': token})
        if not token_data:
            return False
        
        current_expiry = datetime.fromisoformat(token_data['expired_at'])
        new_expiry = current_expiry + timedelta(days=additional_days)
        
        result = self.collection.update_one(
            {'token': token},
            {'$set': {'expired_at': new_expiry.isoformat()}}
        )
        return result.modified_count > 0

    def cleanup_expired_tokens(self) -> int:
        now = datetime.utcnow().isoformat()
        result = self.collection.update_many(
            {'is_active': True, 'expired_at': {'$lt': now}},
            {'$set': {'is_active': False}}
        )
        return result.modified_count
