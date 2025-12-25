"""
Security & Privacy Service - Trust Layer
Handles edge privacy with zero-knowledge storage, blockchain-based voice DNA,
and identity shield for content ownership verification

v3.0+
"""

import hashlib
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import logging
import json
from enum import Enum

logger = logging.getLogger(__name__)


class PrivacyMode(str, Enum):
    """Privacy protection modes"""
    EDGE_PRIVATE = "edge_private"  # Local device only
    ENCRYPTED_CLOUD = "encrypted_cloud"  # E2E encrypted cloud
    ZERO_KNOWLEDGE = "zero_knowledge"  # Server has no access to plaintext
    DECENTRALIZED = "decentralized"  # IPFS/blockchain distributed


class VoiceDNAVerification(str, Enum):
    """Voice DNA verification status"""
    VERIFIED = "verified"
    PENDING = "pending"
    FAILED = "failed"
    REVOKED = "revoked"


@dataclass
class MemoryEncryptionKey:
    """Encryption key for memory storage"""
    key_id: str
    key_material: str  # Encrypted
    created_at: datetime
    expires_at: Optional[datetime] = None
    algorithm: str = "AES-256-GCM"
    storage_location: str = "edge"  # edge, local_device, encrypted_cloud


@dataclass
class VoiceDNA:
    """Voice biometric fingerprint for identity verification"""
    user_id: str
    voice_dna_id: str
    created_at: datetime
    
    # Voice characteristics
    fundamental_frequency: float  # Hz
    formant_frequencies: List[float]  # First 3-4 formants
    mfcc_profile: List[float]  # Mel-Frequency Cepstral Coefficients
    prosody_pattern: Dict  # Rhythm, stress patterns
    
    # Blockchain integration
    blockchain_hash: str  # Immutable identity on blockchain
    smart_contract_address: Optional[str] = None
    verification_status: VoiceDNAVerification = VoiceDNAVerification.PENDING
    authorized_networks: List[str] = field(default_factory=list)
    revocation_certificate: Optional[str] = None
    
    # Security
    nonce: str = ""  # For replay attack prevention
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class ContentOwnershipProof:
    """Proof that content is authorized for use by voice DNA holder"""
    proof_id: str
    voice_dna_id: str
    content_hash: str  # SHA-256 of content
    timestamp: datetime
    blockchain_tx_hash: str  # Transaction on blockchain
    signatures: List[str] = field(default_factory=list)  # Multi-sig if needed
    expiration: Optional[datetime] = None


class EdgePrivacyEngine:
    """
    Manages on-device storage of sensitive data
    Zero-knowledge architecture - server has no access to plaintext
    """
    
    def __init__(self):
        self.local_memory_store: Dict[str, any] = {}
        self.encryption_keys: Dict[str, MemoryEncryptionKey] = {}
        self.privacy_mode = PrivacyMode.EDGE_PRIVATE
        logger.info("Edge Privacy Engine initialized (on-device storage)")
    
    def create_encryption_key(
        self,
        user_id: str,
        key_material: str,
        expires_in_days: Optional[int] = None
    ) -> str:
        """
        Create encryption key for local device storage
        Key never leaves device
        """
        key_id = f"key_{user_id}_{int(datetime.now().timestamp())}"
        
        expiration = None
        if expires_in_days:
            from datetime import timedelta
            expiration = datetime.now() + timedelta(days=expires_in_days)
        
        # In production, use proper key derivation (PBKDF2, etc.)
        encrypted_material = hashlib.sha256(key_material.encode()).hexdigest()
        
        key = MemoryEncryptionKey(
            key_id=key_id,
            key_material=encrypted_material,
            created_at=datetime.now(),
            expires_at=expiration,
            storage_location="edge"  # Always on device
        )
        
        self.encryption_keys[key_id] = key
        
        logger.info(f"Created encryption key {key_id} for local storage")
        return key_id
    
    def store_sensitive_memory(
        self,
        user_id: str,
        memory_content: str,
        encryption_key_id: str,
        memory_type: str = "private"
    ) -> str:
        """
        Store sensitive memory locally with encryption
        Never transmitted to server unencrypted
        """
        if encryption_key_id not in self.encryption_keys:
            return {"error": "Invalid encryption key"}
        
        key = self.encryption_keys[encryption_key_id]
        
        # Simulate encryption (in production, use actual AES-256-GCM)
        encrypted_content = hashlib.sha256(memory_content.encode()).hexdigest()
        
        memory_id = f"mem_edge_{user_id}_{len(self.local_memory_store)}"
        
        self.local_memory_store[memory_id] = {
            "user_id": user_id,
            "encrypted_content": encrypted_content,
            "encryption_key_id": encryption_key_id,
            "memory_type": memory_type,
            "stored_at": datetime.now().isoformat(),
            "storage_location": "local_device",
            "accessible_only_locally": True,
        }
        
        logger.info(f"Stored encrypted memory {memory_id} on local device")
        return memory_id
    
    def decrypt_local_memory(
        self,
        memory_id: str,
        encryption_key: str
    ) -> Optional[str]:
        """
        Decrypt memory on local device
        Only possible with correct encryption key
        """
        if memory_id not in self.local_memory_store:
            logger.warning(f"Memory {memory_id} not found")
            return None
        
        memory = self.local_memory_store[memory_id]
        
        # Verify key matches
        if not self._verify_decryption_key(memory["encryption_key_id"], encryption_key):
            logger.warning(f"Decryption key mismatch for {memory_id}")
            return None
        
        # In production, use actual AES-256-GCM decryption
        decrypted = f"[DECRYPTED] {memory['encrypted_content'][:32]}..."
        
        logger.info(f"Decrypted memory {memory_id} on local device")
        return decrypted
    
    def _verify_decryption_key(self, key_id: str, provided_key: str) -> bool:
        """Verify that provided key matches stored key"""
        if key_id not in self.encryption_keys:
            return False
        
        key = self.encryption_keys[key_id]
        provided_hash = hashlib.sha256(provided_key.encode()).hexdigest()
        
        return provided_hash == key.key_material


class VoiceDNAEngine:
    """
    Blockchain-based Voice DNA for identity verification
    Ensures only the owner can authorize creation of content using their voice
    """
    
    def __init__(self):
        self.voice_dnas: Dict[str, VoiceDNA] = {}
        self.ownership_proofs: Dict[str, ContentOwnershipProof] = {}
        self.blockchain_pending: List[Dict] = []
        logger.info("Voice DNA Engine initialized (blockchain-based identity)")
    
    def register_voice_dna(
        self,
        user_id: str,
        voice_sample_features: Dict
    ) -> str:
        """
        Register user's voice biometric on blockchain
        Creates immutable identity
        
        Args:
            user_id: User ID
            voice_sample_features: Dict with voice characteristics
        
        Returns:
            Voice DNA ID
        """
        voice_dna_id = f"voicedna_{user_id}_{int(datetime.now().timestamp())}"
        
        # Extract voice features
        features = voice_sample_features
        
        # Generate blockchain hash
        feature_string = json.dumps(features, sort_keys=True)
        blockchain_hash = hashlib.sha256(feature_string.encode()).hexdigest()
        
        voice_dna = VoiceDNA(
            user_id=user_id,
            voice_dna_id=voice_dna_id,
            created_at=datetime.now(),
            fundamental_frequency=features.get("f0", 120.0),
            formant_frequencies=features.get("formants", [700, 1220, 2600]),
            mfcc_profile=features.get("mfcc", [0.0] * 13),
            prosody_pattern=features.get("prosody", {}),
            blockchain_hash=blockchain_hash,
            verification_status=VoiceDNAVerification.PENDING,
            nonce=hashlib.sha256(str(datetime.now()).encode()).hexdigest(),
        )
        
        self.voice_dnas[voice_dna_id] = voice_dna
        
        # Queue for blockchain registration
        self.blockchain_pending.append({
            "type": "voice_dna_registration",
            "voice_dna_id": voice_dna_id,
            "hash": blockchain_hash,
            "timestamp": datetime.now().isoformat(),
        })
        
        logger.info(f"Registered Voice DNA {voice_dna_id} (pending blockchain confirmation)")
        
        return voice_dna_id
    
    def verify_voice_ownership(
        self,
        voice_dna_id: str,
        audio_sample: List[float],
        threshold: float = 0.85
    ) -> Tuple[bool, float]:
        """
        Verify that voice matches registered Voice DNA
        Used to authorize content creation
        
        Args:
            voice_dna_id: Registered Voice DNA ID
            audio_sample: Audio sample to verify
            threshold: Similarity threshold (0-1)
        
        Returns:
            Tuple of (verified, similarity_score)
        """
        if voice_dna_id not in self.voice_dnas:
            return False, 0.0
        
        voice_dna = self.voice_dnas[voice_dna_id]
        
        # Extract features from sample
        # Simplified feature extraction
        import numpy as np
        sample_array = np.array(audio_sample)
        
        # Simulate voice matching
        # In production, use proper voice biometric matching
        similarity = self._compute_voice_similarity(voice_dna, sample_array)
        
        verified = similarity >= threshold
        
        if verified:
            logger.info(f"Voice verification successful for {voice_dna_id} (score: {similarity:.2f})")
        else:
            logger.warning(f"Voice verification failed for {voice_dna_id} (score: {similarity:.2f})")
        
        return verified, similarity
    
    def _compute_voice_similarity(self, voice_dna: VoiceDNA, sample: any) -> float:
        """Compute similarity between Voice DNA and sample"""
        # Simplified: random score for demo
        import random
        return 0.7 + random.random() * 0.25  # Range 0.7-0.95
    
    def create_content_ownership_proof(
        self,
        voice_dna_id: str,
        content_hash: str,
        signature: str
    ) -> str:
        """
        Create blockchain proof that content is authorized by Voice DNA owner
        
        Args:
            voice_dna_id: Voice DNA ID
            content_hash: SHA-256 hash of content
            signature: Digital signature
        
        Returns:
            Proof ID
        """
        if voice_dna_id not in self.voice_dnas:
            logger.error(f"Voice DNA {voice_dna_id} not found")
            return None
        
        proof_id = f"proof_{voice_dna_id}_{int(datetime.now().timestamp())}"
        
        # Simulate blockchain transaction
        tx_hash = hashlib.sha256(
            f"{proof_id}{content_hash}{datetime.now().isoformat()}".encode()
        ).hexdigest()
        
        proof = ContentOwnershipProof(
            proof_id=proof_id,
            voice_dna_id=voice_dna_id,
            content_hash=content_hash,
            timestamp=datetime.now(),
            blockchain_tx_hash=tx_hash,
            signatures=[signature],
        )
        
        self.ownership_proofs[proof_id] = proof
        
        # Queue for blockchain
        self.blockchain_pending.append({
            "type": "content_ownership_proof",
            "proof_id": proof_id,
            "tx_hash": tx_hash,
            "timestamp": datetime.now().isoformat(),
        })
        
        logger.info(f"Created content ownership proof {proof_id} (tx: {tx_hash[:16]}...)")
        
        return proof_id
    
    def revoke_voice_dna(
        self,
        voice_dna_id: str,
        revocation_reason: str
    ) -> bool:
        """
        Revoke a Voice DNA to prevent further unauthorized use
        Permanent on blockchain
        """
        if voice_dna_id not in self.voice_dnas:
            return False
        
        voice_dna = self.voice_dnas[voice_dna_id]
        voice_dna.verification_status = VoiceDNAVerification.REVOKED
        voice_dna.revocation_certificate = hashlib.sha256(
            f"{voice_dna_id}{revocation_reason}{datetime.now().isoformat()}".encode()
        ).hexdigest()
        
        # Queue revocation for blockchain
        self.blockchain_pending.append({
            "type": "voice_dna_revocation",
            "voice_dna_id": voice_dna_id,
            "reason": revocation_reason,
            "certificate": voice_dna.revocation_certificate,
            "timestamp": datetime.now().isoformat(),
        })
        
        logger.warning(f"Revoked Voice DNA {voice_dna_id}: {revocation_reason}")
        
        return True


class IdentityShieldEngine:
    """
    Protects user identity and prevents unauthorized deepfakes/voice cloning
    Uses Voice DNA + blockchain for proof of authenticity
    """
    
    def __init__(self, voice_dna_engine: VoiceDNAEngine):
        self.voice_dna_engine = voice_dna_engine
        self.usage_logs: List[Dict] = []
        logger.info("Identity Shield Engine initialized (deepfake prevention)")
    
    def authorize_content_creation(
        self,
        voice_dna_id: str,
        content_type: str,
        distribution_platform: str,
        audio_verification: List[float]
    ) -> Dict:
        """
        Authorize content creation with voice owner verification
        
        Args:
            voice_dna_id: Voice DNA ID
            content_type: Type of content (video, podcast, etc.)
            distribution_platform: Where it will be distributed
            audio_verification: Audio sample for liveness check
        
        Returns:
            Authorization token with blockchain proof
        """
        # Step 1: Verify voice ownership
        verified, score = self.voice_dna_engine.verify_voice_ownership(
            voice_dna_id, audio_verification, threshold=0.85
        )
        
        if not verified:
            logger.warning(f"Authorization denied: voice verification failed ({score:.2f})")
            return {
                "authorized": False,
                "reason": "Voice verification failed",
                "similarity_score": score
            }
        
        # Step 2: Create content ownership proof
        content_hash = hashlib.sha256(
            f"{voice_dna_id}{content_type}{datetime.now().isoformat()}".encode()
        ).hexdigest()
        
        proof_id = self.voice_dna_engine.create_content_ownership_proof(
            voice_dna_id,
            content_hash,
            f"verified_{voice_dna_id}_{datetime.now().timestamp()}"
        )
        
        # Log usage
        self.usage_logs.append({
            "timestamp": datetime.now().isoformat(),
            "voice_dna_id": voice_dna_id,
            "content_type": content_type,
            "platform": distribution_platform,
            "proof_id": proof_id,
            "verification_score": score,
        })
        
        authorization_token = hashlib.sha256(
            f"{voice_dna_id}{proof_id}{datetime.now().timestamp()}".encode()
        ).hexdigest()
        
        logger.info(f"Authorized content creation for {voice_dna_id} on {distribution_platform}")
        
        return {
            "authorized": True,
            "voice_dna_id": voice_dna_id,
            "proof_id": proof_id,
            "authorization_token": authorization_token,
            "content_hash": content_hash,
            "platform": distribution_platform,
            "verified_at": datetime.now().isoformat(),
            "blockchain_proof": True,
        }
    
    def detect_unauthorized_usage(
        self,
        content_hash: str,
        claimed_voice_dna_id: str
    ) -> Dict:
        """
        Detect if content is being used with wrong Voice DNA
        Prevents deepfake/voice cloning abuse
        """
        if claimed_voice_dna_id not in self.voice_dna_engine.voice_dnas:
            return {
                "abuse_detected": True,
                "reason": "Voice DNA not registered",
                "action": "block_content"
            }
        
        # Check if content was authorized for this Voice DNA
        matching_proofs = [
            p for p in self.voice_dna_engine.ownership_proofs.values()
            if p.voice_dna_id == claimed_voice_dna_id and p.content_hash == content_hash
        ]
        
        if not matching_proofs:
            return {
                "abuse_detected": True,
                "reason": "Content not authorized for this Voice DNA",
                "action": "block_content_and_alert_owner",
                "claimed_voice_dna": claimed_voice_dna_id,
            }
        
        return {
            "abuse_detected": False,
            "authorized": True,
            "proof_id": matching_proofs[0].proof_id,
        }


class SecurityPrivacyService:
    """Main service combining edge privacy, Voice DNA, and identity shield"""
    
    def __init__(self):
        self.edge_privacy = EdgePrivacyEngine()
        self.voice_dna = VoiceDNAEngine()
        self.identity_shield = IdentityShieldEngine(self.voice_dna)
        logger.info("Security & Privacy Service initialized")
    
    async def protect_user_memory(
        self,
        user_id: str,
        memory_content: str,
        privacy_level: str = "edge_private"
    ) -> Dict:
        """Protect memory with appropriate encryption"""
        key_id = self.edge_privacy.create_encryption_key(user_id, memory_content)
        memory_id = self.edge_privacy.store_sensitive_memory(
            user_id, memory_content, key_id, privacy_level
        )
        
        return {
            "memory_id": memory_id,
            "privacy_level": privacy_level,
            "encryption_key_id": key_id,
            "protected": True,
        }
    
    async def register_voice_identity(
        self,
        user_id: str,
        voice_features: Dict
    ) -> Dict:
        """Register voice for content authorization"""
        voice_dna_id = self.voice_dna.register_voice_dna(user_id, voice_features)
        
        return {
            "voice_dna_id": voice_dna_id,
            "registered": True,
            "status": "pending_blockchain_confirmation",
        }
    
    async def authorize_content_usage(
        self,
        voice_dna_id: str,
        content_type: str,
        platform: str,
        audio_sample: List[float]
    ) -> Dict:
        """Authorize content creation with identity shield"""
        return self.identity_shield.authorize_content_creation(
            voice_dna_id, content_type, platform, audio_sample
        )
