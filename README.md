# summarizer-server

# Credentials for ML Model Registry Access
- create a SP 
- give contributor role to that SP
- create a secret in K8s namespace
- configure deployment yml to use the secret env vars