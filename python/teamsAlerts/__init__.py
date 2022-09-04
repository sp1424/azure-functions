import os
import azure.functions as func
import json

from urllib import request, parse


def main(req: func.HttpRequest) -> func.HttpResponse:

    req_body = req.get_json()
    essential_data = req_body.get("data").get("essentials")

    title = essential_data.get("monitorCondition")
    alert_id = essential_data.get("alertId")
    alert_rule = essential_data.get("alertRule")
    severity = essential_data.get("severity")
    signal_type = essential_data.get("signalType")
    monitoring_service = essential_data.get("monitoringService")
    alert_target_id = essential_data.get("alertTargetIDs")[0]
    original_alert_id = essential_data.get("originAlertId")
    fired_time = essential_data.get("firedDateTime")
    resolved_time = essential_data.get("resolvedDateTime")

    message = {
    "@type": "MessageCard",
    "@context": "http://schema.org/extensions",
    "themeColor": "0076D7",
    "summary": title,
    "sections": [{
        "activityTitle": title,
        "activitySubtitle": "Alert: " + alert_id,
        "facts": [
          {
            "name": "Alert Rule",
            "value": alert_rule
          }, 
          {
            "name": "Severity",
            "value": severity
          },
          {
            "name": "Signal Type",
            "value": signal_type
          },
          {
            "name": "Monitoring Service",
            "value": monitoring_service
          },
          {
            "name": "Alert Target Id",
            "value": alert_target_id
          },
          {
            "name": "Original Alert Id",
            "value": original_alert_id
          },
          {
            "name": "Fired at",
            "value": fired_time
          },
          {
            "name": "Resolved at",
            "value": resolved_time
          },
        ],
     }],
    }

    url = os.getenv("webhookurl")

    if url is None:
     return func.HttpResponse(
     "Webhook missing from environment variables",
     status_code=400
    )

    encoded_data = json.dumps(message).encode()
    req = request.Request(url, data=encoded_data)
    req.add_header("Content-Type", "application/json")
    request.urlopen(req)

    return func.HttpResponse(
         "",
         status_code=200
    )