from workflows import STATE_GENERATION, STATE_DOWNLOAD_HCP_DATA, STATE_AI_PROCESSING, STATE_GENERATE_TEMPLATES, STATE_TEMPLATES_READY
from workflows import STATE_APPROVALS, STATE_MEDICAL_APPROVAL, STATE_COMPLIANCE_APPROVAL, STATE_BRAND_APPROVAL, STATE_TEMPLATES_APPROVED
from workflows import STATE_DISTRIBUTION, STATE_FIND_TARGET_DOCTORS, STATE_GENERATE_TAILORED_COMMS, STATE_SEND_COMMUNICATION, STATE_DISTRIBUTED

def generate_graph_data(workflow): 
    elements = [
        { "id": '0', "data": { "label": STATE_GENERATION                }, "type":"input", "style": { "background": "lightgreen" if workflow.state_machine.isStateDone(STATE_GENERATION) else ("white" if workflow.is_active() else "pink"), "width": 200 }, "position": { "x": 100, "y": 100 } },
        { "id": '1', "data": { "label": STATE_DOWNLOAD_HCP_DATA         }, "type":"input", "style": { "background": "lightgreen" if workflow.state_machine.isStateDone(STATE_DOWNLOAD_HCP_DATA) else ("white" if workflow.is_active() else "pink"), "width": 200 }, "position": { "x": 100, "y": 200 } },
        { "id": '2', "data": { "label": STATE_AI_PROCESSING             }, "type":"input", "style": { "background": "lightgreen" if workflow.state_machine.isStateDone(STATE_AI_PROCESSING) else ("white" if workflow.is_active() else "pink"), "width": 200 }, "position": { "x": 100, "y": 250 } },
        { "id": '3', "data": { "label": STATE_GENERATE_TEMPLATES        }, "type":"input", "style": { "background": "lightgreen" if workflow.state_machine.isStateDone(STATE_GENERATE_TEMPLATES) else ("white" if workflow.is_active() else "pink"), "width": 200 }, "position": { "x": 100, "y": 300 } },
        { "id": '4', "data": { "label": STATE_TEMPLATES_READY           }, "type":"input", "style": { "background": "lightgreen" if workflow.state_machine.isStateDone(STATE_TEMPLATES_READY) else ("white" if workflow.is_active() else "pink"), "width": 200 }, "position": { "x": 100, "y": 400 } },
        { "id": '5', "data": { "label": STATE_APPROVALS                 }, "type":"input", "style": { "background": "lightgreen" if workflow.state_machine.isStateDone(STATE_APPROVALS) else ("white" if workflow.is_active() else "pink"), "width": 200 }, "position": { "x": 400, "y": 100 } },
        { "id": '6', "data": { "label": STATE_MEDICAL_APPROVAL          }, "type":"input", "style": { "background": "lightgreen" if workflow.state_machine.isStateDone(STATE_MEDICAL_APPROVAL) else ("white" if workflow.is_active() else "pink"), "width": 200 }, "position": { "x": 400, "y": 200 } },
        { "id": '7', "data": { "label": STATE_COMPLIANCE_APPROVAL       }, "type":"input", "style": { "background": "lightgreen" if workflow.state_machine.isStateDone(STATE_COMPLIANCE_APPROVAL) else ("white" if workflow.is_active() else "pink"), "width": 200 }, "position": { "x": 400, "y": 250 } },
        { "id": '8', "data": { "label": STATE_BRAND_APPROVAL            }, "type":"input", "style": { "background": "lightgreen" if workflow.state_machine.isStateDone(STATE_BRAND_APPROVAL) else ("white" if workflow.is_active() else "pink"), "width": 200 }, "position": { "x": 400, "y": 300 } },
        { "id": '9', "data": { "label": STATE_TEMPLATES_APPROVED        }, "type":"input", "style": { "background": "lightgreen" if workflow.state_machine.isStateDone(STATE_TEMPLATES_APPROVED) else ("white" if workflow.is_active() else "pink"), "width": 200 }, "position": { "x": 400, "y": 400 } },
        { "id": '10', "data": { "label": STATE_DISTRIBUTION             }, "type":"input", "style": { "background": "lightgreen" if workflow.state_machine.isStateDone(STATE_DISTRIBUTION) else ("white" if workflow.is_active() else "pink"), "width": 200 }, "position": { "x": 700, "y": 100 } },
        { "id": '11', "data": { "label": STATE_FIND_TARGET_DOCTORS      }, "type":"input", "style": { "background": "lightgreen" if workflow.state_machine.isStateDone(STATE_FIND_TARGET_DOCTORS) else ("white" if workflow.is_active() else "pink"), "width": 200 }, "position": { "x": 700, "y": 200 } },
        { "id": '12', "data": { "label": STATE_GENERATE_TAILORED_COMMS  }, "type":"input", "style": { "background": "lightgreen" if workflow.state_machine.isStateDone(STATE_GENERATE_TAILORED_COMMS) else ("white" if workflow.is_active() else "pink"), "width": 200 }, "position": { "x": 700, "y": 250 } },
        { "id": '13', "data": { "label": STATE_SEND_COMMUNICATION       }, "type":"input", "style": { "background": "lightgreen" if workflow.state_machine.isStateDone(STATE_SEND_COMMUNICATION) else ("white" if workflow.is_active() else "pink"), "width": 200 }, "position": { "x": 700, "y": 300 } },
        { "id": '14', "data": { "label": STATE_DISTRIBUTED              }, "type":"input", "style": { "background": "lightgreen" if workflow.state_machine.isStateDone(STATE_DISTRIBUTED) else ("white" if workflow.is_active() else "pink"), "width": 200 }, "position": { "x": 700, "y": 400 } },
        { "id": 'e0-1',     "source": '0',  "target": '1',  "animated": True },
        { "id": 'e1-2',     "source": '1',  "target": '2',  "animated": True },
        { "id": 'e2-3',     "source": '2',  "target": '3',  "animated": True },
        { "id": 'e3-4',     "source": '3',  "target": '4',  "animated": True },
        { "id": 'e4-5',     "source": '4',  "target": '5',  "animated": True },
        { "id": 'e5-6',     "source": '5',  "target": '6',  "animated": True },
        { "id": 'e6-7',     "source": '6',  "target": '7',  "animated": True },
        { "id": 'e7-8',     "source": '7',  "target": '8',  "animated": True },
        { "id": 'e8-9',     "source": '8',  "target": '9',  "animated": True },
        { "id": 'e9-10',    "source": '9',  "target": '10', "animated": True },
        { "id": 'e10-11',   "source": '10', "target": '11', "animated": True },
        { "id": 'e11-12',   "source": '11', "target": '12', "animated": True },
        { "id": 'e12-13',   "source": '12', "target": '13', "animated": True },
        { "id": 'e13-14',   "source": '13', "target": '14', "animated": True },
    ]

    return elements