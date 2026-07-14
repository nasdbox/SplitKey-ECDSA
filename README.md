# 🗝️ SplitKey-ECDSA

![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Cryptography](https://img.shields.io/badge/crypto-secp256k1-orange)

A Python implementation demonstrating the core mathematics behind **Threshold ECDSA**. This project illustrates how to split a private key across multiple parties and perform homomorphic computations without ever reconstructing the full key on a single device.

> **⚠️ SECURITY WARNING:** This repository is strictly for **educational purposes** to demonstrate the interactions between the secp256k1 curve, Paillier Homomorphic Encryption, and Schnorr Zero-Knowledge Proofs. It lacks the complex Range Proofs required to prevent modular arithmetic overflow attacks in production. **Do not use this to secure actual cryptocurrency.**

---

## Features

* **Additive Key Splitting:** Distributes a secp256k1 private key into multiple secret shares.
* **Paillier Homomorphic Encryption:** Allows parties to multiply their key shares cryptographically without revealing the underlying plaintext values.
* **Schnorr Zero-Knowledge Proofs (ZKPs):** Utilizes the Fiat-Shamir heuristic so parties can mathematically prove they own their secret share without exposing it.

---

## Quick Start

### Prerequisites
You will need Python 3.9+ and the following cryptographic libraries:

```bash
pip install ecdsa phe
