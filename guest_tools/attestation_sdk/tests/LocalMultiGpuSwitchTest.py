#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2023 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
#
from nv_attestation_sdk import attestation
import os
import json


client = attestation.Attestation()
client.set_name("thisNode1")
client.set_nonce("931d8dd0add203ac3d8b4fbde75e115278eefcdceac5b87671a748f32364dfcb")

print ("[LocalGPUTest] node name :", client.get_name())
file = "policies/local/NVGPULocalPolicyExample.json"

client.add_verifier(attestation.Devices.GPU, attestation.Environment.LOCAL, "", "")

print(client.get_verifiers())

print ("[LocalGPUTest] call get_evidence()")
evidence_list = client.get_evidence()

print ("[LocalGPUTest] call attest() - expecting True")
print("[LocalGPUTest] call attest() - result : ", client.attest(evidence_list))
print ("[LocalGPUTest] token : "+str(client.get_token()))
print ("[LocalGPUTest] call validate_token() - expecting True")

with open(os.path.join(os.path.dirname(__file__), file)) as json_file:
    json_data = json.load(json_file)
    att_result_policy = json.dumps(json_data)
print ("[LocalGPUTest] call validate_token() - result: ", client.validate_token(att_result_policy))

client.decode_token(client.get_token())
client.clear_verifiers()

print ("[LocalSwitchTest] node name :", client.get_name())

client.set_nonce("931d8dd0add203ac3d8b4fbde75e115278eefcdceac5b87671a748f32364dfcb")

client.add_verifier(attestation.Devices.SWITCH, attestation.Environment.LOCAL, "", "")

evidence_list = client.get_evidence()

client.attest(evidence_list)
file = "policies/local/NVSwitchLocalPolicyExample.json"
print ("[LocalSwitchTest] token : "+str(client.get_token()))

with open(os.path.join(os.path.dirname(__file__), file)) as json_file:
    json_data = json.load(json_file)
    remote_att_result_policy = json.dumps(json_data)
print(client.validate_token(remote_att_result_policy))

client.decode_token(client.get_token())

