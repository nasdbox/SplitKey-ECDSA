from mpc.party import Party
from mpc.crypto import util, n

def run():
	print("=== Stage 1: Key Generation ===")
	a = Party("A")
	b = Party("B")
	joint_pub_key = a.public_share + b.public_share
	print(f"Aggregated Public Key calculated successfully.")
	
	print("\n=== Stage 2: Identity Verification (ZKP) ===")
	R_a, s_a = a.prove_ownership()
	if b.verify_peer(a.public_share, R_a, s_a):
		print("B successfully verified A's ZKP")
	else:
		print("A's ZKP validation failed")
		return
	
	print("\n=== Stage 3: Homomorphic Computation ===")
	enc_a_share = a.paillier_pub.encrypt(a.secret_share)
	
	# B prepares his binding factor locally
	b_blinding_factor = util.randrange(n)
	# processing the ciphertext homomorphically
	enc_blinded_result = b.compute_homomorphic_step(enc_a_share, b_blinding_factor)
	decrypted_secret = a.decrypt_payload(enc_blinded_result)
	print("Homomorphic interaction success. Decrypted verification payload handled.")
	

if __name__ == "__main__":
	run()
