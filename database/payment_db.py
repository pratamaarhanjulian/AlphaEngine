"""
Payment Database Module for AUREA PRIME ELITE
Handles payment records and verification
"""

from datetime import datetime
from typing import Optional, Dict, List, Any


class PaymentDB:
    def __init__(self, db_connection):
        self.db = db_connection
        self.collection = self.db.get_collection('payments')

    def create_payment(self, user_id: str, username: str, first_name: str,
                       package: str, duration: str, tier: str, 
                       amount: int, proof_url: str = None) -> Dict[str, Any]:
        payment_data = {
            'user_id': user_id,
            'username': username,
            'first_name': first_name,
            'package': package,
            'duration': duration,
            'tier': tier,
            'amount': amount,
            'proof_url': proof_url,
            'status': 'PENDING',
            'verified_by': None,
            'verified_at': None,
            'rejection_reason': None,
            'created_at': datetime.utcnow().isoformat()
        }
        result = self.collection.insert_one(payment_data)
        payment_data['_id'] = str(result.inserted_id)
        return payment_data

    def get_pending_payments(self) -> List[Dict[str, Any]]:
        return list(self.collection.find({'status': 'PENDING'}).sort('created_at', 1))

    def approve_payment(self, payment_id: str, admin_id: str) -> bool:
        result = self.collection.update_one(
            {'_id': payment_id},
            {'$set': {'status': 'APPROVED', 'verified_by': admin_id, 'verified_at': datetime.utcnow().isoformat()}}
        )
        return result.modified_count > 0

    def reject_payment(self, payment_id: str, admin_id: str, reason: str) -> bool:
        result = self.collection.update_one(
            {'_id': payment_id},
            {'$set': {'status': 'REJECTED', 'verified_by': admin_id, 'verified_at': datetime.utcnow().isoformat(), 'rejection_reason': reason}}
        )
        return result.modified_count > 0

    def get_payment_stats(self) -> Dict[str, Any]:
        total = self.collection.count_documents({})
        pending = self.collection.count_documents({'status': 'PENDING'})
        approved = self.collection.count_documents({'status': 'APPROVED'})
        rejected = self.collection.count_documents({'status': 'REJECTED'})
        return {'total': total, 'pending': pending, 'approved': approved, 'rejected': rejected}
