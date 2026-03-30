#!/usr/bin/env python3
"""
Generates the three Apple Shortcuts .shortcut files for the AI assistant guide.
Outputs to the shortcuts/ directory.
"""

import plistlib
import uuid
import os

API_KEY_PLACEHOLDER = 'YOUR_CLAUDE_API_KEY_HERE'
MODEL = 'claude-haiku-4-5-20251001'
CLAUDE_URL = 'https://api.anthropic.com/v1/messages'

HEADERS = {
    'x-api-key': API_KEY_PLACEHOLDER,
    'anthropic-version': '2023-06-01',
    'content-type': 'application/json',
}

def uid():
    return str(uuid.uuid4()).upper()

def text_token(s):
    """A plain text value in Shortcuts."""
    return {
        'Value': {'string': s, 'attachmentsByRange': {}},
        'WFSerializationType': 'WFTextTokenString',
    }

def var_token(output_uuid, output_name='Output'):
    """A reference to a previous action's output, used inside text/string fields."""
    return {
        'Value': {
            'string': '\ufffc',
            'attachmentsByRange': {
                '{0, 1}': {
                    'Type': 'ActionOutput',
                    'OutputUUID': output_uuid,
                    'OutputName': output_name,
                }
            },
        },
        'WFSerializationType': 'WFTextTokenString',
    }

def var_input(output_uuid, output_name='Output'):
    """A reference to a previous action's output, used as a direct input parameter."""
    return {
        'Value': {
            'Type': 'ActionOutput',
            'OutputUUID': output_uuid,
            'OutputName': output_name,
        },
        'WFSerializationType': 'WFTokenAttachmentParameterState',
    }

def dict_value(items):
    """A Shortcuts dictionary value."""
    return {
        'Value': {'WFDictionaryFieldValueItems': items},
        'WFSerializationType': 'WFDictionaryFieldValue',
    }

def array_value(items):
    """A Shortcuts array value."""
    return {
        'Value': {'WFArrayParameterItems': items},
        'WFSerializationType': 'WFArrayParameterValue',
    }

def str_field(key, value_token):
    """A string key/value pair for a dictionary."""
    return {'WFItemType': 0, 'WFKey': text_token(key), 'WFValue': value_token}

def dict_field(key, sub_items):
    """A dictionary key/value pair where value is a dictionary."""
    return {'WFItemType': 1, 'WFKey': text_token(key), 'WFValue': dict_value(sub_items)}

def array_field(key, array_items):
    """A dictionary key/value pair where value is an array."""
    return {'WFItemType': 2, 'WFKey': text_token(key), 'WFValue': array_value(array_items)}

def dict_item_in_array(sub_items):
    """A dictionary element inside an array."""
    return {'WFItemType': 1, 'WFValue': dict_value(sub_items)}

def headers_value(headers_dict):
    items = [{'WFItemType': 0, 'WFKey': text_token(k), 'WFValue': text_token(v)}
             for k, v in headers_dict.items()]
    return {'Value': {'WFDictionaryFieldValueItems': items}, 'WFSerializationType': 'WFDictionaryFieldValue'}

def http_post_action(out_uuid, url, headers, body_items, out_name='Claude Response'):
    return {
        'WFWorkflowActionIdentifier': 'is.workflow.actions.downloadurl',
        'WFWorkflowActionParameters': {
            'UUID': out_uuid,
            'CustomOutputName': out_name,
            'WFHTTPMethod': 'POST',
            'WFURL': text_token(url),
            'WFHTTPHeaders': headers_value(headers),
            'WFHTTPBodyType': 'JSON',
            'WFHTTPBody': dict_value(body_items),
        },
    }

def claude_messages_body(content_value):
    """Build the Claude API JSON body items with given content value."""
    return [
        str_field('model', text_token(MODEL)),
        str_field('max_tokens', text_token('1024')),
        array_field('messages', [
            dict_item_in_array([
                str_field('role', text_token('user')),
                str_field('content', content_value),
            ])
        ]),
    ]

def claude_vision_body(base64_data_token, question_token):
    """Build Claude API body with image + text content array."""
    return [
        str_field('model', text_token(MODEL)),
        str_field('max_tokens', text_token('1024')),
        array_field('messages', [
            dict_item_in_array([
                str_field('role', text_token('user')),
                {
                    'WFItemType': 2,
                    'WFKey': text_token('content'),
                    'WFValue': array_value([
                        dict_item_in_array([
                            str_field('type', text_token('image')),
                            dict_field('source', [
                                str_field('type', text_token('base64')),
                                str_field('media_type', text_token('image/png')),
                                str_field('data', base64_data_token),
                            ]),
                        ]),
                        dict_item_in_array([
                            str_field('type', text_token('text')),
                            str_field('text', question_token),
                        ]),
                    ]),
                },
            ])
        ]),
    ]

def parse_response_actions(request_uuid, request_name='Claude Response'):
    """Actions to extract text from Claude response: content[0].text"""
    content_uuid = uid()
    item_uuid = uid()
    text_uuid = uid()
    return [
        {
            'WFWorkflowActionIdentifier': 'is.workflow.actions.getvalueforkey',
            'WFWorkflowActionParameters': {
                'UUID': content_uuid,
                'CustomOutputName': 'Response Content',
                'WFInput': var_input(request_uuid, request_name),
                'WFDictionaryKey': text_token('content'),
            },
        },
        {
            'WFWorkflowActionIdentifier': 'is.workflow.actions.getitemfromlist',
            'WFWorkflowActionParameters': {
                'UUID': item_uuid,
                'CustomOutputName': 'First Content Block',
                'WFItemSpecifier': 'First Item',
                'WFInput': var_input(content_uuid, 'Response Content'),
            },
        },
        {
            'WFWorkflowActionIdentifier': 'is.workflow.actions.getvalueforkey',
            'WFWorkflowActionParameters': {
                'UUID': text_uuid,
                'CustomOutputName': 'Response Text',
                'WFInput': var_input(item_uuid, 'First Content Block'),
                'WFDictionaryKey': text_token('text'),
            },
        },
        {
            'WFWorkflowActionIdentifier': 'is.workflow.actions.showresult',
            'WFWorkflowActionParameters': {
                'Text': var_token(text_uuid, 'Response Text'),
            },
        },
    ]

def wrap_shortcut(actions, name):
    return {
        'WFWorkflowClientVersion': '1160.0.2',
        'WFWorkflowMinimumClientVersion': 900,
        'WFWorkflowMinimumClientVersionString': '900',
        'WFWorkflowName': name,
        'WFWorkflowIcon': {
            'WFWorkflowIconGlyphNumber': 59511,
            'WFWorkflowIconStartColor': -1524986881,
        },
        'WFWorkflowImportQuestions': [],
        'WFWorkflowInputContentItemClasses': ['WFStringContentItem'],
        'WFWorkflowTypes': ['ActionExtension', 'NCWidget'],
        'WFWorkflowActions': actions,
    }

# ──────────────────────────────────────────────────────────────────────────────
# Shortcut 1: AI Text Helper
# Copy text → Claude API → Show Result
# ──────────────────────────────────────────────────────────────────────────────

def build_shortcut_1():
    clipboard_uuid = uid()
    request_uuid = uid()

    actions = [
        {
            'WFWorkflowActionIdentifier': 'is.workflow.actions.getclipboard',
            'WFWorkflowActionParameters': {
                'UUID': clipboard_uuid,
                'CustomOutputName': 'Clipboard',
            },
        },
        http_post_action(
            request_uuid,
            CLAUDE_URL,
            HEADERS,
            claude_messages_body(var_token(clipboard_uuid, 'Clipboard')),
        ),
        *parse_response_actions(request_uuid),
    ]
    return wrap_shortcut(actions, 'AI Text Helper')

# ──────────────────────────────────────────────────────────────────────────────
# Shortcut 2: AI Ask (Type or Voice)
# Menu → Ask for Input OR Dictate Text → Claude API → Show Result
# ──────────────────────────────────────────────────────────────────────────────

def build_shortcut_2():
    group_uuid = uid()
    ask_uuid = uid()
    dictate_uuid = uid()
    request_uuid = uid()

    actions = [
        # Menu start
        {
            'WFWorkflowActionIdentifier': 'is.workflow.actions.choosefrommenu',
            'WFWorkflowActionParameters': {
                'GroupingIdentifier': group_uuid,
                'WFControlFlowMode': 0,
                'WFMenuPrompt': text_token('How do you want to ask?'),
                'WFMenuItems': ['Type', 'Speak'],
            },
        },
        # Branch: Type
        {
            'WFWorkflowActionIdentifier': 'is.workflow.actions.choosefrommenu',
            'WFWorkflowActionParameters': {
                'GroupingIdentifier': group_uuid,
                'WFControlFlowMode': 1,
                'WFMenuItem': 'Type',
            },
        },
        {
            'WFWorkflowActionIdentifier': 'is.workflow.actions.ask',
            'WFWorkflowActionParameters': {
                'UUID': ask_uuid,
                'CustomOutputName': 'Provided Input',
                'WFAskActionPrompt': text_token("What's your question?"),
                'WFInputType': 'Text',
                'WFAskActionDefaultAnswer': text_token(''),
            },
        },
        # Branch: Speak
        {
            'WFWorkflowActionIdentifier': 'is.workflow.actions.choosefrommenu',
            'WFWorkflowActionParameters': {
                'GroupingIdentifier': group_uuid,
                'WFControlFlowMode': 1,
                'WFMenuItem': 'Speak',
            },
        },
        {
            'WFWorkflowActionIdentifier': 'is.workflow.actions.dictatetext',
            'WFWorkflowActionParameters': {
                'UUID': dictate_uuid,
                'CustomOutputName': 'Provided Input',
                'WFSpeechLanguage': 'default',
                'WFDictateTextStopListening': 'After Short Pause',
            },
        },
        # Menu end
        {
            'WFWorkflowActionIdentifier': 'is.workflow.actions.choosefrommenu',
            'WFWorkflowActionParameters': {
                'GroupingIdentifier': group_uuid,
                'WFControlFlowMode': 2,
            },
        },
        # After menu: send whichever input was captured to Claude
        # The magic variable here uses ask_uuid; Shortcuts resolves the active branch output
        http_post_action(
            request_uuid,
            CLAUDE_URL,
            HEADERS,
            claude_messages_body(var_token(ask_uuid, 'Provided Input')),
        ),
        *parse_response_actions(request_uuid),
    ]
    return wrap_shortcut(actions, 'AI Ask')

# ──────────────────────────────────────────────────────────────────────────────
# Shortcut 3: AI See My Screen
# Screenshot → Base64 → Ask question → Claude vision API → Show Result
# ──────────────────────────────────────────────────────────────────────────────

def build_shortcut_3():
    screenshot_uuid = uid()
    base64_uuid = uid()
    question_uuid = uid()
    request_uuid = uid()

    actions = [
        # Take screenshot
        {
            'WFWorkflowActionIdentifier': 'is.workflow.actions.takescreenshot',
            'WFWorkflowActionParameters': {
                'UUID': screenshot_uuid,
                'CustomOutputName': 'Screenshot',
            },
        },
        # Wait 0.5s
        {
            'WFWorkflowActionIdentifier': 'is.workflow.actions.delay',
            'WFWorkflowActionParameters': {
                'WFDelayTime': 0.5,
            },
        },
        # Base64 encode the screenshot
        {
            'WFWorkflowActionIdentifier': 'is.workflow.actions.base64encode',
            'WFWorkflowActionParameters': {
                'UUID': base64_uuid,
                'CustomOutputName': 'Base64 Screenshot',
                'WFEncodeMode': 'Encode',
                'WFBase64LineBreakMode': 'None',
                'WFInput': var_input(screenshot_uuid, 'Screenshot'),
            },
        },
        # Ask question
        {
            'WFWorkflowActionIdentifier': 'is.workflow.actions.ask',
            'WFWorkflowActionParameters': {
                'UUID': question_uuid,
                'CustomOutputName': 'Question',
                'WFAskActionPrompt': text_token("What's your question about this screen?"),
                'WFInputType': 'Text',
                'WFAskActionDefaultAnswer': text_token(''),
            },
        },
        # POST to Claude vision API
        http_post_action(
            request_uuid,
            CLAUDE_URL,
            HEADERS,
            claude_vision_body(
                var_token(base64_uuid, 'Base64 Screenshot'),
                var_token(question_uuid, 'Question'),
            ),
        ),
        *parse_response_actions(request_uuid),
    ]
    return wrap_shortcut(actions, 'AI See My Screen')

# ──────────────────────────────────────────────────────────────────────────────
# Write files
# ──────────────────────────────────────────────────────────────────────────────

out_dir = os.path.join(os.path.dirname(__file__), 'shortcuts')
os.makedirs(out_dir, exist_ok=True)

shortcuts = {
    'AI-Text-Helper.shortcut': build_shortcut_1(),
    'AI-Ask.shortcut': build_shortcut_2(),
    'AI-See-My-Screen.shortcut': build_shortcut_3(),
}

for filename, data in shortcuts.items():
    path = os.path.join(out_dir, filename)
    with open(path, 'wb') as f:
        plistlib.dump(data, f, fmt=plistlib.FMT_BINARY)
    print(f'Written: {path}')

print('Done.')
