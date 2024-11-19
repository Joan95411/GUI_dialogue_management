import re
import json

def convert_file_to_json(file_path):
    node_data_array = []
    link_data_array = []
    node_key = 0
    with open(file_path, 'r') as file:
        lines = file.readlines()

    blocks = "".join(lines).split('===')
    for block in blocks:
        if not block.strip():
            continue
        lines = block.strip().split('\n')
        group = {
            "horiz": False,
            'isGroup': True,
            'key': node_key,
            'text': lines[0][len('title: '):],
        }
        node_data_array.append(group)
        node_key += 1
        text_lines = []
        capture_text = False
        for line in lines:
            if line.startswith('---'):
                capture_text = True
                continue
            elif line.startswith('[['):
                capture_text=False
                parts = re.findall(r'\[\[(.*?)\|(.*?)\]\]', line)
                for part in parts:
                    node={
                        'key': node_key,
                        'group':group['key'],
                        'text': part[0]
                    }
                    link_data_array.append({
                        'from': node['key'],
                        'fromPort': 'R',
                        'to': part[1],
                        'toPort': 'L',
                    })

                    node_data_array.append(node)

                    node_key += 1

            elif capture_text:
                text_lines.append(line)

        if text_lines:
            node_data_array.append( {
                'group': group['key'],
                'category': 'Doc',
                'key': group['text'],
                'text': ' '.join(text_lines)
            })
        node_key += 1

    json_data = {
        "class": "GraphLinksModel",
        "linkFromPortIdProperty": "fromPort",
        "linkToPortIdProperty": "toPort",
        "nodeDataArray": node_data_array,
        "linkDataArray": link_data_array
    }

    return json.dumps(json_data, indent=4)


file_path = 'templates/extra-info-hart-HCM.wool'
json_data = convert_file_to_json(file_path)



with open('templates/model.json', 'w') as file:
    file.write(json_data)