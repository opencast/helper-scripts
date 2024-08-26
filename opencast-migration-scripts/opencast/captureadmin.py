#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json


def get_agents(opencast_admin_client):
    url = '/capture-admin/agents.json'
    response = opencast_admin_client.get(url)
    response.raise_for_status()
    agents = response.json()
    if not isinstance(agents, dict):
        return
    agent_obj_or_list = agents.get('agents', dict()).get('agent', None)
    if not agent_obj_or_list:
        return
    if isinstance(agent_obj_or_list, dict) and 'name' in agent_obj_or_list:
        agents_list = [agent_obj_or_list]
    else:
        agents_list = agent_obj_or_list
    for agent in agents_list:
        name = agent.get('name')
        state = agent.get('state')
        url = agent.get('url')
        if agent.get('capabilities', None):
            agent_capabilities = agent.get('capabilities', dict()).get('item', None)
            if agent_capabilities is not None:
                if isinstance(agent_capabilities, list):
                    capabilities = {item['key']: item['value'] for item in agent_capabilities}
                elif isinstance(agent_capabilities, dict):
                    capabilities = {agent_capabilities['key']: agent_capabilities['value']}
                else:
                    raise TypeError(f'Agent capabilities is in invalid format: {agent_capabilities}')
        else:
            capabilities = {}
        yield {
            'name': name,
            'state': state,
            'url': url,
            'capabilities': capabilities,
        }


def update_agent_status(opencast_admin_client, agent_name, agent_url='http://127.0.0.1/', agent_state='offline'):
    url = f'/capture-admin/agents/{agent_name}'
    params = {
        'address': agent_url,
        'state': agent_state,
    }
    response = opencast_admin_client.post(url, data=params)
    response.raise_for_status()


def set_agent_capabilities(opencast_admin_client, agent_name, agent_capabilities):
    url = f'/capture-admin/agents/{agent_name}/configuration'
    params = {
        'configuration': json.dumps(agent_capabilities),
    }
    response = opencast_admin_client.post(url, data=params)
    response.raise_for_status()
