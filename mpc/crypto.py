import hashlib
from ecdsa import SECP256k1, util

# Global curve parameters
CURVE = SECP256k1
n = CURVE.order # total number of valid points on the curve (a massive prime number)
# all scalar math in ECDSA will follows modulo n to stay within the mathematical group
G = CURVE.generator # publicly known (x, y) coordinate point on the curve y^2 = x^3 + 7 (mod p)

# generates a Deterministic challenge
def hash_to_int(*args) -> int:
	""" Generates a deterministic integer challenge via Fiat-Shamir Heuristic """
	h = hashlib.sha256()
	for arg in args:
		if isinstance(arg, int):
			h.update(arg.to_bytes(32, "big"))
		elif hasattr(arg, "to_bytes"):
			# if implementation support is available
			h.update(arg.to_bytes())
	
	return int.from_bytes(h.digest(), "big")

def gen_schnorr_zkp(secret_share: int, public_share) -> tuple:
	# generating a non-interactive zkp of a secret share
	# it allows any party p_i to prove that it knows the secret scalar share (x_a) without ever revealing it
	k = util.randrange(n) # picking a nonce out of the finite field (mod n)
	R = k * G # a commitment of the random choice by taking the base point G to get an elliptic curve point R without ever revealing k
	
	# return a challenge by hashing the public parameters G and public key x_a alongside his commitment R
	# uniquely binds the proof to his identity and this specific session
	c = hash_to_int(G.x(), G.y(), public_share.x(), public_share.y(), R.x(), R.y()) 
	
	# calculting the response by masking the secret key his x_a and further algebrically secured by (mod n)
	s = (k + c * secret_share) % n
	
	return R, s # the zkp proof
	
def verify_schnorr_zkp(public_share, R, s) -> bool:
	""" verifies a Schnorr zkp for secp256k1 """

	# another party verifying it using elliptic math using the public share x_a and his proof (R, s)
	# btw same calculating as in generating the zkp but also for verifying it by other party
	c = hash_to_int(G.x(), G.y(), public_share.x(), public_share.y(), R.x(), R.y())
	lhs = s*G
	rhs = R + (c * public_share)

	# the mathematics
	# lhs = s.G
	# lhs = (k + c.X_a).G
	# lhs = (k.G) + (c.X_a.G)
	# lhs = R + c.x_a = rhs (proved!!!)
	# conclusion: if two curve points match, other party has the mathematical certainty that the first party knows X_a without ever learning a single bit of it

	return lsh == rhs

	
