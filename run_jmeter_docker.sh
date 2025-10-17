#!/usr/bin/env bash
# Ejecutar JMeter (Docker) en modo no-GUI apuntando al ALB DNS
set -euo pipefail

JMETER_IMAGE="${JMETER_IMAGE:-justb4/jmeter:5.4.1}"
JMETER_TEST_PLAN="${JMETER_TEST_PLAN:-Load-tests.jmx}"  # usa el .jmx del repo Jmeter-test
ALB_DNS="${ALB_DNS:-REPLACE_WITH_ALB_DNS}"               # reemplaza con DNS del ALB (o exportar ALB_DNS)

RESULTS="${RESULTS:-results.jtl}"
REPORT_DIR="${REPORT_DIR:-jmeter-report}"

if [ "${ALB_DNS}" = "REPLACE_WITH_ALB_DNS" ]; then
  echo "Set ALB_DNS env var or edit this script to set ALB_DNS."
  exit 1
fi

# Si el .jmx tiene un marker REPLACE_HOST, lo reemplazamos (si no, edítalo en GUI)
if grep -q "REPLACE_WITH_ALB_DNS" "${JMETER_TEST_PLAN}" >/dev/null 2>&1; then
  sed -i "s/REPLACE_WITH_ALB_DNS/${ALB_DNS}/g" "${JMETER_TEST_PLAN}"
fi

# Ejecutar container de JMeter
docker run --rm -v "$(pwd)":/tests -w /tests ${JMETER_IMAGE} \
  -n -t /tests/${JMETER_TEST_PLAN} -l /tests/${RESULTS} -e -o /tests/${REPORT_DIR}

echo "Resultados guardados: ${RESULTS}, HTML report: ${REPORT_DIR}"
