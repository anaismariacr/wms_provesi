#!/usr/bin/env bash
# Crear Security Groups para el laboratorio
set -euo pipefail

REGION="${REGION:-us-east-1}"
VPC_ID="$(aws ec2 describe-vpcs --filters Name=isDefault,Values=true --region "${REGION}" --query 'Vpcs[0].VpcId' --output text)"

echo "Region: ${REGION}, VPC: ${VPC_ID}"

# 1) trafico-ssh
SG_SSH_NAME="trafico-ssh"
SG_SSH_ID=$(aws ec2 create-security-group --group-name "${SG_SSH_NAME}" --description "SSH access" --vpc-id "${VPC_ID}" --region "${REGION}" --query 'GroupId' --output text || true)
aws ec2 authorize-security-group-ingress --group-id "${SG_SSH_ID}" --protocol tcp --port 22 --cidr 0.0.0.0/0 --region "${REGION}" || true
echo "SG SSH: ${SG_SSH_ID}"

# 2) trafico-db (postgres 5432)
SG_DB_NAME="trafico-db"
SG_DB_ID=$(aws ec2 create-security-group --group-name "${SG_DB_NAME}" --description "DB access" --vpc-id "${VPC_ID}" --region "${REGION}" --query 'GroupId' --output text || true)
aws ec2 authorize-security-group-ingress --group-id "${SG_DB_ID}" --protocol tcp --port 5432 --cidr 0.0.0.0/0 --region "${REGION}" || true
echo "SG DB: ${SG_DB_ID}"

# 3) trafico-http (app port 8080)
SG_HTTP_NAME="trafico-http"
SG_HTTP_ID=$(aws ec2 create-security-group --group-name "${SG_HTTP_NAME}" --description "HTTP 8080" --vpc-id "${VPC_ID}" --region "${REGION}" --query 'GroupId' --output text || true)
aws ec2 authorize-security-group-ingress --group-id "${SG_HTTP_ID}" --protocol tcp --port 8080 --cidr 0.0.0.0/0 --region "${REGION}" || true
echo "SG HTTP: ${SG_HTTP_ID}"

# 4) trafico-lb (allow HTTP from internet to LB)
SG_LB_NAME="trafico-lb"
SG_LB_ID=$(aws ec2 create-security-group --group-name "${SG_LB_NAME}" --description "LB security group (internet)" --vpc-id "${VPC_ID}" --region "${REGION}" --query 'GroupId' --output text || true)
aws ec2 authorize-security-group-ingress --group-id "${SG_LB_ID}" --protocol tcp --port 80 --cidr 0.0.0.0/0 --region "${REGION}" || true
echo "SG LB: ${SG_LB_ID}"

echo "Created/ensured SGs: ${SG_SSH_ID}, ${SG_DB_ID}, ${SG_HTTP_ID}, ${SG_LB_ID}"
