# tests/test_mpc.py
import pytest
from mpc.party import Party
from mpc.crypto import hash_to_int

def test_zkp_verification():
    alice = Party("Alice")
    bob = Party("Bob")
    
    R, s = alice.prove_ownership()
    assert bob.verify_peer(alice.public_share, R, s) == True

def test_hash_determinism():
    assert hash_to_int(123, 456) == hash_to_int(123, 456)
    assert hash_to_int(123) != hash_to_int(456)
