"""
Comprehensive Tests for AuraStudio Omni v3.0+
Tests for all advanced features: Digital Physique, Neural Persona, Autonomous Agency, Security/Privacy

Run with: pytest tests/test_advanced_v3.py -v --tb=short
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'api'))

import pytest
import asyncio
import numpy as np
from datetime import datetime, timedelta
from app.services.digital_physique import (
    DigitalPhysiqueService, InteractionType, ClothingType, InverseKinematicsEngine
)
from app.services.neural_persona import (
    NeuralPersonaService, UserBiometrics, LongTermMemoryEngine
)
from app.services.autonomous_agency import (
    AutonomousAgencyService, AutonomousAgentEngine, DigitalImmortalityEngine, SocialPlatform
)
from app.services.security_privacy import (
    SecurityPrivacyService, EdgePrivacyEngine, VoiceDNAEngine
)


# ==================== DIGITAL PHYSIQUE TESTS ====================

class TestDigitalPhysique:
    """Test suite for Digital Physique service"""
    
    @pytest.fixture
    def service(self):
        return DigitalPhysiqueService()
    
    def test_ik_engine_initialization(self):
        """Test IK engine creates successfully"""
        engine = InverseKinematicsEngine()
        assert engine.max_iterations == 100
        assert engine.tolerance == 0.001
    
    def test_ik_hand_grasp(self, service):
        """Test IK solving for grasp interaction"""
        hand_base = np.array([0.2, 1.7, 0.1])
        target = np.array([0.5, 1.5, 0.2])
        
        hand_pose = service.ik_engine.solve_hand_to_target(
            hand_base, target, None, InteractionType.GRASP
        )
        
        assert hand_pose is not None
        assert "thumb" in hand_pose.finger_angles
        assert hand_pose.grip_strength > 0.0  # Should have some grip
    
    def test_ik_hand_pinch(self, service):
        """Test IK solving for pinch interaction"""
        hand_base = np.array([0.2, 1.7, 0.1])
        target = np.array([0.3, 1.6, 0.15])
        
        hand_pose = service.ik_engine.solve_hand_to_target(
            hand_base, target, None, InteractionType.PINCH
        )
        
        assert hand_pose.finger_angles["thumb"] >= 0
        assert hand_pose.finger_angles["index"] >= 0
        assert hand_pose.grip_strength < 0.8  # Pinch is lighter
    
    def test_object_interaction_endpoint(self, service):
        """Test object interaction endpoint"""
        import asyncio
        result = asyncio.run(service.handle_object_interaction(
            "avatar_1", "cup_1", InteractionType.GRASP,
            [0.5, 1.5, 0.2], None
        ))
        
        assert result["avatar_id"] == "avatar_1"
        assert result["object_id"] == "cup_1"
        assert "hand_pose" in result
    
    def test_skin_subsurface_scattering(self, service):
        """Test skin response to lighting"""
        light_dir = np.array([1, 0, 0])
        response = service.atmosphere_engine.calculate_skin_response(light_dir)
        
        assert "sss_intensity" in response
        assert 0 <= response["sss_intensity"] <= 1
        assert response["sss_color_r"] > 0
    
    def test_cloth_physics_simulation(self, service):
        """Test neural cloth physics simulation"""
        cloth_state = service.atmosphere_engine.simulate_cloth_physics(
            ClothingType.SILK, wind_speed=5.0, rain_intensity=0.3
        )
        
        assert cloth_state.material == ClothingType.SILK
        assert 0 <= cloth_state.wind_influence <= 1
        assert 0 <= cloth_state.rain_saturation <= 1
    
    def test_vocalization_injection(self, service):
        """Test non-verbal vocalization injection"""
        import asyncio
        text = "Hello world. This is great! How are you?"
        result = asyncio.run(service.enhance_speech_with_vocalizations(
            text, emotion="excited", pace=1.0
        ))
        
        assert "original_text" in result
        assert "enhanced_text" in result
        assert "vocalizations" in result
        assert len(result["vocalizations"]) > 0


# ==================== NEURAL PERSONA TESTS ====================

class TestNeuralPersona:
    """Test suite for Neural Persona service"""
    
    @pytest.fixture
    def service(self):
        return NeuralPersonaService()
    
    def test_memory_storage(self, service):
        """Test storing memory with vector embedding"""
        embedding = [0.1] * 1536  # 1536-dim OpenAI embedding
        
        memory_id = service.memory_engine.store_memory(
            "user_1", "User likes coffee", embedding, "preference"
        )
        
        assert memory_id.startswith("mem_")
        assert "user_1" in memory_id
    
    def test_memory_retrieval(self, service):
        """Test retrieving similar memories"""
        embedding = [0.1] * 1536
        
        # Store a few memories
        service.memory_engine.store_memory("user_1", "Coffee preference", embedding)
        service.memory_engine.store_memory("user_1", "Tea preference", embedding)
        
        # Retrieve
        results = service.memory_engine.retrieve_memories("user_1", embedding, top_k=2)
        
        assert len(results) <= 2
    
    def test_user_profile_building(self, service):
        """Test user profile accumulation from memories"""
        embedding = [0.1] * 1536
        
        service.memory_engine.store_memory("user_1", "Likes hiking", embedding, "preference")
        service.memory_engine.store_memory("user_1", "Prefers tea", embedding, "preference")
        service.memory_engine.store_memory("user_1", "Heart rate elevated", embedding, "health")
        
        profile = service.memory_engine.get_user_profile("user_1")
        
        assert len(profile["preferences"]) == 2
        assert len(profile["health_notes"]) == 1
    
    def test_biometric_analysis(self, service):
        """Test affective computing on biometrics"""
        import asyncio
        result = asyncio.run(service.analyze_user_health(
            "user_1",
            {
                "heart_rate": 100,
                "hrv": 30,
                "skin_r": 0.6,
                "skin_g": 0.5,
                "skin_b": 0.4,
                "pupil_dilation": 0.6,
                "blink_rate": 25,
            }
        ))
        
        assert "analysis" in result
        assert "stress_level" in result["analysis"]
        assert "emotion" in result["analysis"]
        assert 0 <= result["analysis"]["stress_level"] <= 1
    
    def test_stress_detection(self, service):
        """Test stress level detection from biometrics"""
        biometrics = UserBiometrics(
            timestamp=datetime.now(),
            heart_rate=140,  # High
            heart_rate_variability=15,  # Low
            skin_color_r=0.6,
            skin_color_g=0.5,
            skin_color_b=0.4,
            pupil_dilation=0.8,  # Dilated
            blink_rate=30,  # High
        )
        
        analysis = service.affective_engine.analyze_biometrics(biometrics)
        
        # Should detect high stress
        assert analysis["stress_level"] > 0.5
        assert analysis["emotion"] in ["stressed", "panic"]
    
    def test_health_suggestions(self, service):
        """Test proactive health suggestions"""
        biometrics = UserBiometrics(
            timestamp=datetime.now(),
            heart_rate=130,
            heart_rate_variability=20,
            skin_color_r=0.6,
            skin_color_g=0.5,
            skin_color_b=0.4,
            pupil_dilation=0.5,
            blink_rate=20,
        )
        
        analysis = service.affective_engine.analyze_biometrics(biometrics)
        suggestions = analysis["proactive_suggestions"]
        
        assert len(suggestions) > 0


# ==================== AUTONOMOUS AGENCY TESTS ====================

class TestAutonomousAgency:
    """Test suite for Autonomous Agency service"""
    
    @pytest.fixture
    def service(self):
        return AutonomousAgencyService()
    
    def test_schedule_social_post(self, service):
        """Test scheduling social media post"""
        from datetime import timedelta
        
        scheduled_time = datetime.now() + timedelta(hours=1)
        
        post_id = service.agent_engine.schedule_social_post(
            "Check out this amazing content!",
            SocialPlatform.TIKTOK,
            scheduled_time,
            hashtags=["ai", "avatar"]
        )
        
        assert post_id.startswith("post_")
    
    def test_go_live_stream(self, service):
        """Test starting live stream"""
        import asyncio
        session_id = asyncio.run(service.agent_engine.go_live(
            SocialPlatform.INSTAGRAM,
            "Q&A Session",
            "friendly",
            30
        ))
        
        assert session_id.startswith("live_")
        assert session_id in service.agent_engine.active_sessions
    
    def test_chat_interaction(self, service):
        """Test chat message processing"""
        import asyncio
        # Create session first
        session_id = asyncio.run(service.agent_engine.go_live(
            SocialPlatform.INSTAGRAM,
            "Q&A",
            "friendly"
        ))
        
        # Process chat
        response = asyncio.run(service.agent_engine.process_chat_interaction(
            session_id, "user123", "Hi there!"
        ))
        
        assert "response" in response
        assert len(response["response"]) > 0
    
    def test_product_setup(self, service):
        """Test product setup for sales"""
        product_id = service.agent_engine.set_up_product_sales(
            "Exclusive AI Course",
            "Learn AI from avatar expert",
            99.99,
            "Limited time offer!",
            15.0
        )
        
        assert product_id.startswith("prod_")
        assert product_id in service.agent_engine.products
    
    def test_autonomous_product_sale(self, service):
        """Test autonomous product sale"""
        import asyncio
        product_id = service.agent_engine.set_up_product_sales(
            "Course", "Description", 50.0, "Pitch", 10.0
        )
        
        result = asyncio.run(service.agent_engine.sell_product_autonomously(
            product_id, "customer1", SocialPlatform.TIKTOK
        ))
        
        assert "commission_earned" in result
        assert result["commission_earned"] == 5.0  # 10% of $50
    
    def test_create_digital_legacy(self, service):
        """Test digital legacy creation"""
        life_data = {
            "communication_style": "warm",
            "interests": ["technology", "philosophy"],
            "catchphrases": ["That's amazing!"],
            "humor": "witty",
            "core_values": ["honesty", "kindness"],
        }
        
        legacy_id = service.immortality_engine.create_digital_legacy(
            "user_1", "interactive", life_data,
            ["Live authentically", "Help others"]
        )
        
        assert legacy_id.startswith("legacy_")
    
    def test_interactive_legacy_response(self, service):
        """Test interacting with legacy"""
        import asyncio
        # Create legacy first
        life_data = {
            "communication_style": "warm",
            "interests": ["tech"],
            "core_values": ["honesty"],
        }
        
        legacy_id = service.immortality_engine.create_digital_legacy(
            "user_1", "interactive", life_data
        )
        
        # Interact
        response = asyncio.run(service.immortality_engine.interactive_legacy_response(
            legacy_id, "I miss you", "John"
        ))
        
        assert "legacy_response" in response
        assert "John" in response["legacy_response"]


# ==================== SECURITY & PRIVACY TESTS ====================

class TestSecurityPrivacy:
    """Test suite for Security & Privacy service"""
    
    @pytest.fixture
    def service(self):
        return SecurityPrivacyService()
    
    def test_encryption_key_creation(self, service):
        """Test encryption key creation"""
        key_id = service.edge_privacy.create_encryption_key(
            "user_1", "secret_key_material"
        )
        
        assert key_id.startswith("key_")
        assert key_id in service.edge_privacy.encryption_keys
    
    def test_local_memory_storage(self, service):
        """Test storing sensitive memory locally"""
        key_id = service.edge_privacy.create_encryption_key("user_1", "key_material")
        
        memory_id = service.edge_privacy.store_sensitive_memory(
            "user_1", "My health record", key_id, "health"
        )
        
        assert memory_id.startswith("mem_edge_")
    
    def test_memory_decryption(self, service):
        """Test decrypting local memory"""
        key_material = "test_key"
        key_id = service.edge_privacy.create_encryption_key("user_1", key_material)
        
        memory_id = service.edge_privacy.store_sensitive_memory(
            "user_1", "Secret data", key_id
        )
        
        # Decrypt
        result = service.edge_privacy.decrypt_local_memory(memory_id, key_material)
        
        assert result is not None
    
    def test_voice_dna_registration(self, service):
        """Test Voice DNA registration"""
        voice_features = {
            "f0": 120.0,
            "formants": [700, 1220, 2600],
            "mfcc": [0.1] * 13,
            "prosody": {"pitch_range": 80}
        }
        
        voice_dna_id = service.voice_dna.register_voice_dna("user_1", voice_features)
        
        assert voice_dna_id.startswith("voicedna_")
        assert voice_dna_id in service.voice_dna.voice_dnas
    
    def test_voice_ownership_verification(self, service):
        """Test voice ownership verification"""
        voice_features = {
            "f0": 120.0,
            "formants": [700, 1220, 2600],
            "mfcc": [0.1] * 13,
            "prosody": {}
        }
        
        voice_dna_id = service.voice_dna.register_voice_dna("user_1", voice_features)
        
        # Verify
        verified, score = service.voice_dna.verify_voice_ownership(
            voice_dna_id, [0.1] * 16000
        )
        
        # Should succeed with high probability
        assert isinstance(verified, bool)
        assert 0 <= score <= 1
    
    def test_content_ownership_proof(self, service):
        """Test creating content ownership proof"""
        voice_features = {
            "f0": 120.0,
            "formants": [700, 1220, 2600],
            "mfcc": [0.1] * 13,
            "prosody": {}
        }
        
        voice_dna_id = service.voice_dna.register_voice_dna("user_1", voice_features)
        
        proof_id = service.voice_dna.create_content_ownership_proof(
            voice_dna_id,
            "abc123",  # content hash
            "signature"
        )
        
        assert proof_id.startswith("proof_")
    
    def test_unauthorized_usage_detection(self, service):
        """Test detecting unauthorized content usage"""
        voice_features = {
            "f0": 120.0,
            "formants": [700, 1220, 2600],
            "mfcc": [0.1] * 13,
            "prosody": {}
        }
        
        voice_dna_id = service.voice_dna.register_voice_dna("user_1", voice_features)
        
        # Check for unauthorized usage with wrong hash
        result = service.identity_shield.detect_unauthorized_usage(
            "wrong_hash", voice_dna_id
        )
        
        assert result["abuse_detected"] == True
    
    def test_protect_memory_endpoint(self, service):
        """Test memory protection endpoint"""
        import asyncio
        result = asyncio.run(service.protect_user_memory(
            "user_1", "My secret memory", "edge_private"
        ))
        
        assert "memory_id" in result
        assert result["protected"] == True
    
    def test_voice_dna_registration_endpoint(self, service):
        """Test voice DNA registration endpoint"""
        import asyncio
        result = asyncio.run(service.register_voice_identity(
            "user_1",
            {
                "f0": 120.0,
                "formants": [700, 1220, 2600],
                "mfcc": [0.1] * 13,
                "prosody": {}
            }
        ))
        
        assert "voice_dna_id" in result
        assert result["registered"] == True


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
