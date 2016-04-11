function decryptSecret(cipher, privateKey, keyCipher, ivCipher) {
  // Create the encryption object.
  var rsa = new JSEncrypt();

  // Set the private.
  rsa.setPrivateKey(privateKey);

  // Get the AES key
  var key = CryptoJS.enc.Hex.parse(rsa.decrypt(keyCipher));
  var iv = CryptoJS.enc.Hex.parse(rsa.decrypt(ivCipher));

  // Get the input and crypted values.
  return CryptoJS.AES.decrypt(cipher, key, { iv: iv }).toString(CryptoJS.enc.Utf8);
}

function encryptSecret(plaintext, publicKey) {
  // Create the encryption object.
  var rsa = new JSEncrypt();

  // Set the public key
  rsa.setPublicKey(publicKey);

  // Generate the AES key
  var key = CryptoJS.lib.WordArray.random(32);
  var iv = CryptoJS.lib.WordArray.random(32);
  var encryptedKey = rsa.encrypt(CryptoJS.enc.Hex.stringify(key));
  var encryptedIv = rsa.encrypt(CryptoJS.enc.Hex.stringify(iv));

  // Get the input and crypted values.
  var encryptedValue = CryptoJS.AES.encrypt(plaintext, key, { iv: iv }).toString();
  return {
    'key': encryptedKey,
    'iv': encryptedIv,
    'value': encryptedValue
  };
}
