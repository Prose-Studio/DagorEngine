// Crypto without OpenSSL, for the programs that never encrypt (the DAGOR_NO_CRYPTO target property: the daScript AOT
// compiler, which links the networking code only for its types)
#include <dagCrypto/cipher.h>
#include <dagCrypto/rand.h>
#include <dagCrypto/ssl.h>
#include <debug/dag_fatal.h>

namespace crypto
{

void init_ssl(InitSslFlags) {}
void cleanup_ssl() {}

void rand_bytes(uint8_t *, size_t) { DAG_FATAL("crypto: rand_bytes in a program without crypto (DAGOR_NO_CRYPTO)"); }

ISymmetricCipher *create_cipher_aes(Mode, KeySize)
{
  DAG_FATAL("crypto: create_cipher_aes in a program without crypto (DAGOR_NO_CRYPTO)");
  return nullptr;
}

} // namespace crypto
