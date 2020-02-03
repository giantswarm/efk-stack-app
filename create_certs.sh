#!/bin/bash

./certs_certstrap/certstrap init --common-name "root" --expires "5 years" --organization "Giant Swarm" --passphrase ""
./certs_certstrap/certstrap request-cert --common-name "transport" --passphrase "" 
./certs_certstrap/certstrap sign transport --CA "root" --expires "5 years"

openssl pkcs8 -v1 "PBE-SHA1-3DES" -in ./out/transport.key -topk8 -out ./out/transport.pem -nocrypt