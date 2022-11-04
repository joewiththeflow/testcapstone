#!/bin/bash
export DATABASE_URL="postgresql://joe@localhost:5432/capstone"
export TEST_DATABASE_URL="postgresql://joe@localhost:5432/capstone_test"
export AUTH0_DOMAIN="dev-zk1xgmkt.us.auth0.com"
export ALGORITHMS=["RS256"]
export API_AUDIENCE="capstone"
echo "setup.sh script executed successfully!"
