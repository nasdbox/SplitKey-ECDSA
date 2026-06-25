from ecdsa import util
from phe import paillier
from .crypto import n, G, generate_schnorr_zkp, verify_schnorr_zkp

class Party:
	def __init__(self, name: str):
		self.name = name
		self.secret_share = util.randrange(n)
		self.public_share = self.secret_share * G
	
		# Paillier homomorphic setup
		self.paillier_pub, self.paillier_priv = paillier.generate_paillier_keypair(n_length=2048)
		
	def prove_ownership(self) -> tuple:
		# create zkp of local share ownership
		return gen_schnorr_zkp(self.secret_share, self.public_share)

	def verify_peer(self, peer_public_share, R, s) -> bool:
		return verify_schnorr_zkp(peer_public_share, R, s)
	
	def compute_homomorphic_step(self, encrypted_share, external_blind: int) -> tuple:
        	"""
        	Executes b's step: takes an encrypted payload, homomorphically multiplies 
        	its own secret share, and blinds it to maintain privacy.
       		"""
	        # E(x_A)^x_B = E(x_A * x_B)
	        enc_cross_term = encrypted_share * self.secret_share
	        # E(x_A * x_B) + E(r) = E(x_A * x_B + r)
	        enc_blinded_term = enc_cross_term + external_blind
	        return enc_blinded_term

    	def decrypt_payload(self, encrypted_payload) -> int:
        	"""Decrypts a homomorphically processed ciphertext."""
        	return self.paillier_priv.decrypt(encrypted_payload)
