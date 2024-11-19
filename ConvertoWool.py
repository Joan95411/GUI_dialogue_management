import json

def convert_json_to_wool(file_path):
    with open(file_path, 'r') as file:
        json_data = json.load(file)

    node_data_array = json_data.get("nodeDataArray", [])
    link_data_array = json_data.get("linkDataArray", [])

    wool_data=[]
    wool_file = ""

    group_nodes = [node for node in node_data_array if node.get("isGroup", False)]
    doc_nodes = [node for node in node_data_array if node.get("category", "") == "Doc"]
    all_nodes = [node for node in node_data_array if node not in group_nodes ]
    for link in link_data_array:
        from_node = next((node for node in node_data_array if node["key"] == link["from"]), None)
        to_node = next((node for node in node_data_array if node["key"] == link["to"]), None)
        to_node['des']=next((node['text'] for node in group_nodes if node["key"] == to_node["group"]), None)
        for node in all_nodes:
            if node['key']==from_node['key']:
                node['to']=to_node['des']
    print(all_nodes)
    for group in group_nodes:
        wool_meta = {
            "key": "",
            "title": "",
            "speaker": "Agent",
            "position": "",
            "Doc": "",
            "Option": []
        }
        wool_meta['key']=group['key']
        wool_meta['title']=group['text']
        for doc in doc_nodes:
            if doc['group']==group['key']:
                wool_meta['Doc']=doc['text']
                x=doc['loc'].split()[0]
                y=doc['loc'].split()[1]
                wool_meta['position']=f"{x},{y}"
        for pat in all_nodes:
            if pat['group']==group['key']:
                if 'to' in pat:
                    if pat in doc_nodes:
                        wool_meta['Option'].append(f"[[{pat['to']}]]")
                    else:
                        wool_meta['Option'].append(f"[[{pat['text']}|{pat['to']}]]")
                else:
                    if pat not in doc_nodes:
                        wool_meta['Option'].append(f"[[{pat['text']}|Start]]")
        wool_data.append(wool_meta)
    #print(wool_data)
    for wool in wool_data:
        wool_file +=f"title: {wool['title']}\n"
        wool_file += f"tags: \n"
        wool_file += f"speaker: {wool['speaker']}\n"
        wool_file += f"colorID: 1 \n"
        wool_file += f"position:{wool['position']} \n"
        wool_file += f"---\n"
        wool_file += f"{wool['Doc']}\n\n"
        if len(wool['Option'])>0:
            for op in wool['Option']:
                wool_file += f"{op}\n"
        wool_file += f"===\n"

    return wool_file

# Example usage
wool_file = convert_json_to_wool('templates/model.json')
with open('templates/model.wool', 'w') as file:
    file.write(wool_file)
