#!/usr/bin/env bash
# Lanzar 2 EC2 Ubuntu 24.04 y ejecutar user-data para clonar app y preparar entorno
set -euo pipefail

REGION="${REGION:-us-east-1}"
KEY_NAME="${KEY_NAME:-lab-key}"
INSTANCE_TYPE="${INSTANCE_TYPE:-t2.nano}"
COUNT=2
REPO="https://github.com/anaismariacr/wms_provesi.git"
BRANCH="${BRANCH:-Load-Balancer}"
USER_DATA_FILE="ec2_user_data.txt"
SG_HTTP_NAME="trafico-http"
SG_SSH_NAME="trafico-ssh"

# Obtener default VPC subnet(s) (tomamos 2 subnets para zonas diferentes si disponibles)
SUBNETS=$(aws ec2 describe-subnets --filters "Name=vpc-id,Values=$(aws ec2 describe-vpcs --filters Name=isDefault,Values=true --query 'Vpcs[0].VpcId' --output text --region ${REGION})" --region ${REGION} --query 'Subnets[0:2].SubnetId' --output text)
echo "Subnets: ${SUBNETS}"

# Find latest Ubuntu 24.04 AMI id via SSM parameter (may change por región)
AMI_ID=$(aws ssm get-parameter --name /aws/service/canonical/ubuntu/server/24.04/stable/current/amd64/hvm/ebs-gp2/ami-id --region "${REGION}" --query 'Parameter.Value' --output text)
echo "AMI ID: ${AMI_ID}"

# Ensure key pair exists (create local .pem if not)
if ! aws ec2 describe-key-pairs --key-names "${KEY_NAME}" --region "${REGION}" >/dev/null 2>&1; then
  aws ec2 create-key-pair --key-name "${KEY_NAME}" --query 'KeyMaterial' --output text --region "${REGION}" > "${KEY_NAME}.pem"
  chmod 600 "${KEY_NAME}.pem"
  echo "Created key pair and saved to ${KEY_NAME}.pem"
else
  echo "Key pair ${KEY_NAME} exists"
fi

# Resolve SG ids
SG_SSH_ID=$(aws ec2 describe-security-groups --filters Name=group-name,Values="${SG_SSH_NAME}" --region "${REGION}" --query 'SecurityGroups[0].GroupId' --output text)
SG_HTTP_ID=$(aws ec2 describe-security-groups --filters Name=group-name,Values="${SG_HTTP_NAME}" --region "${REGION}" --query 'SecurityGroups[0].GroupId' --output text)

if [ -z "${SG_SSH_ID}" ] || [ -z "${SG_HTTP_ID}" ]; then
  echo "Security groups missing. Run aws_create_security_groups.sh first."
  exit 1
fi

# Read user-data
if [ ! -f "${USER_DATA_FILE}" ]; then
  echo "User data file ${USER_DATA_FILE} not found."
  exit 1
fi

# Launch instances
INSTANCE_IDS=$(aws ec2 run-instances \
  --image-id "${AMI_ID}" \
  --count "${COUNT}" \
  --instance-type "${INSTANCE_TYPE}" \
  --key-name "${KEY_NAME}" \
  --security-group-ids "${SG_SSH_ID}" "${SG_HTTP_ID}" \
  --user-data file://"${USER_DATA_FILE}" \
  --tag-specifications "ResourceType=instance,Tags=[{Key=Name,Value=monitoring-app-lb}]" \
  --region "${REGION}" \
  --query 'Instances[*].InstanceId' --output text)

echo "Launched instances: ${INSTANCE_IDS}"
echo "Waiting until running..."
aws ec2 wait instance-running --instance-ids ${INSTANCE_IDS} --region "${REGION}"
echo "Instances running. Describe them:"
aws ec2 describe-instances --instance-ids ${INSTANCE_IDS} --region "${REGION}" --query 'Reservations[*].Instances[*].[InstanceId,PublicIpAddress,PrivateIpAddress,State.Name]' --output table

echo "Deberás editar settings.py (DATABASES HOST) en una de las instancias antes de correr migraciones si tu DB está en otra VM."
