"""
Generates a JWT (JSON Web Token) using a Google API Service Account and prints it to the terminal.
"""

import argparse
import time
import os

import google.auth.crypt
import google.auth.jwt

import requests


def generate_jwt(
    sa_keyfile,
    sa_email,
    audience,
    expiry_length,
):
    """Generates a signed JSON Web Token using a Google API Service Account."""

    now = int(time.time())

    # build payload
    payload = {
        "iat": now,
        # expires after 'expiry_length' seconds.
        "exp": now + expiry_length,
        # iss must match 'issuer' in the security configuration in your
        # swagger spec (e.g. service account email). It can be any string.
        "iss":sa_email,
        # aud must be either your Endpoints service name, or match the value
        # specified as the 'x-google-audience' in the OpenAPI document.
        "aud": "https://www.googleapis.com/auth/iam",
        # sub and email should match the service account's email address
        "sub": sa_email,
        "email": sa_email,
    }

    # sign with keyfile
    signer = google.auth.crypt.RSASigner.from_service_account_file(sa_keyfile)
    jwt = google.auth.jwt.encode(signer, payload)

    return jwt


def main():
    """Parses command-line arguments and generates/prints the JWT."""
    parser = argparse.ArgumentParser(
        description="Generate a JWT using a Google API Service Account."
    )
    parser.add_argument(
        "--sa_keyfile",
        required=True,
        help="Path to the Google API Service Account key file (JSON).",
    )
    parser.add_argument(
        "--sa_email",
        default="jwt-signer@db-demo-gke-ent.iam.gserviceaccount.com",
        help="Service account email.",
    )
    parser.add_argument(
        "--audience",
        default="simple-http-server",
        help="Audience for the JWT (e.g., your Endpoints service name).",
    )
    parser.add_argument(
        "--expiry_length",
        type=int,
        default=1800,
        help="Expiry length of the JWT in seconds (default: 1800).",
    )

    args = parser.parse_args()

    # Check if the keyfile exists
    if not os.path.exists(args.sa_keyfile):
        print(f"Error: Service account key file not found: {args.sa_keyfile}")
        return

    jwt = generate_jwt(
        args.sa_keyfile, args.sa_email, args.audience, args.expiry_length
    )
    print("Generated JWT:")
    print(jwt)


if __name__ == "__main__":
    main()
