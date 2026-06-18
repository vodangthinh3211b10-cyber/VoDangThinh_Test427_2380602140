from flask import Flask, request, jsonify

from cipher.ecc import ECCCipher
app = Flask(__name__)

# RSA CIPHER ALGORITHM

ecc_cipher = ECCCipher()


@app.route('/api/ecc/generate_keys', methods=['GET'])
def ecc_generate_keys():
    ecc_cipher.generate_keys()
    return jsonify({'message': 'Keys generated successfully'})

@app.route('/api/ecc/sign', methods=['POST'])
def ecc_sign_message():
    data = request.json
    message = data['message']
    
    # load_keys() của ECC trả về (sk, vk) theo thứ tự private trước, public sau
    private_key, _ = ecc_cipher.load_keys()
    signature = ecc_cipher.sign(message, private_key)
    signature_hex = signature.hex()
    return jsonify({'signature': signature_hex})

@app.route('/api/ecc/verify', methods=['POST'])
def ecc_verify_signature():
    data = request.json
    message = data['message']
    signature_hex = data['signature']
    
    _, public_key = ecc_cipher.load_keys()
    signature = bytes.fromhex(signature_hex)
    is_verified = ecc_cipher.verify(message, signature, public_key)
    return jsonify({'is_verified': is_verified})
# main function
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)