import os
import configparser
from jinja2 import Environment, FileSystemLoader


def get_all_component(pathname):
    cf = configparser.ConfigParser()
    cf.read(pathname)

    component_name_list = cf.get('component', 'name')
    
    return component_name_list.split(',')

def check_component_conf(component_name_list, dir_name):
    valid_componet_list = list()
    for name in component_name_list:
        conf_name = dir_name + name + '_task.conf'
        if os.path.isfile(conf_name):
            print('component [%s] is found'%name)
            valid_componet_list.append(name)
        else:
            print('component [%s] is not found'%name)

    return valid_componet_list

def parse_component_conf(component_conf_name, dir_name):
    print(dir_name + component_conf_name)
    cf = configparser.ConfigParser()
    cf.read(dir_name + component_conf_name)

    component_conf_info = dict()
    component_conf_info['task_name'] = cf.get('basic_info', 'task_name')

    key_list = cf.options('event_id')
    for key in key_list:
        component_conf_info['%s'%key] = cf.get('event_id', '%s'%key)

    print(component_conf_info)

def generate_taskmain_c(templates_dir, target_dir, component_conf_info):
    env = Environment(loader=FileSystemLoader(templates_dir))
    template = env.get_template('templates_taskmain_c.j2')
    
    target_file_name = component_conf_info['task_name'] + '_taskmain.c'
    with open(target_dir + target_file_name, 'w') as fp:
        c_content = template.render(task_name=component_conf_info['task_name'])
        fp.write(c_content)

if __name__ == '__main__':
    cur_dir=os.getcwd()
    conf_dir=cur_dir + r'\conf\\'
    component_name_list = get_all_component(conf_dir + 'component.conf')
    valid_component_list = check_component_conf(component_name_list, conf_dir)

    for component in valid_component_list:
        component_conf_name = component + '_task.conf'
        parse_component_conf(component_conf_name, conf_dir)