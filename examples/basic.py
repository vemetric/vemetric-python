from vemetric import VemetricClient

vemetricClient = VemetricClient(token="WRlW37cPSLUAbXDk76wYU", host="http://localhost:4004")

vemetricClient.track_event(
    "SignupCompleted",
    user_identifier="dmmIrnzUzVMJD03tjCiHXTEEgX6xIPJm",
    event_data={"plan": "ProPython"},
)

vemetricClient.update_user(
    "dmmIrnzUzVMJD03tjCiHXTEEgX6xIPJm",
    user_data={"set": {"plan": "BusinessPython"}},
)

print("✅ events sent")