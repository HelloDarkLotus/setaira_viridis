import os
import configparser
from jinja2 import Environment, FileSystemLoader


class LoadConf:
    def __init__(self):
        cur_dir = os.getcwd()
        self.conf_dir = cur_dir + r'\conf\\'
        self.template_dir = cur_dir + r'\templates\\'
        self.target_dir = cur_dir + r'\target\\'

    def load_component(self):
        cf = configparser.ConfigParser()
        cf.read(self.conf_dir + 'component.conf')
        component_list = cf.get('component', 'name')
        return component_list.split(',')

    def check_component_validation(self, component_list_in_conf):
        valid_component_list = list()
        for name in component_list_in_conf:
            component_conf_name = self.conf_dir + name + '_task.conf'
            if os.path.isfile(component_conf_name):
                print('component [%s] is valid' % name)
                valid_component_list.append(name)
            else:
                print('component [%s] is invalid' % name)

        return valid_component_list

    def generate_store_dir(self, valid_component_list):
        for component in valid_component_list:
            if os.path.exists(self.target_dir + component):
                os.rmdir(self.target_dir + component)

            os.mkdir(self.target_dir + component)

    def parse_component_conf(self, valid_component_list):
        cf = configparser.ConfigParser()
        
        component_info_dict = dict()
        for component_name in valid_component_list:
            cf.read(self.conf_dir + component_name + '_task.conf')
            component_info = dict()
            component_info_dict['%s' % component_name] = component_info
            component_info['task_name'] = cf.get('basic_info', 'task_name')

            state_list = list()
            key_list = cf.options('state')
            for key in key_list:
                state_list.append(cf.get('state', '%s' % key))

            component_info['state'] = state_list

            event_name_list = list()
            key_list = cf.options('event_name')
            for key in key_list:
                event_name_list.append(cf.get('event_name', '%s' % key))

            component_info['event_name'] = event_name_list

        return component_info_dict

    def generate_taskmain_c(self, component_info):
        env = Environment(loader=FileSystemLoader(self.template_dir))
        template = env.get_template('templates_taskmain_c.j2')

        target_file_name = component_info['task_name'] + '_taskmain.c'
        target_file_path = self.target_dir + component_info['task_name'] + r'\\' + target_file_name
        with open(target_file_path, 'w') as f:
            c_file = template.render(task_name=component_info['task_name'])
            f.write(c_file)

    def generate_msg_api_c(self, component_info):
        env = Environment(loader=FileSystemLoader(self.template_dir))
        template = env.get_template('templates_msg_api_c.j2')

        target_file_name = component_info['task_name'] + '_msg_api.c'
        target_file_path = self.target_dir + component_info['task_name'] + r'\\' + target_file_name
        with open(target_file_path, 'w') as f:
            c_file = template.render(task_name=component_info['task_name'], events=component_info['event_name'])
            f.write(c_file)

    def generate_msg_api_h(self, component_info):
        env = Environment(loader=FileSystemLoader(self.template_dir))
        template = env.get_template('templates_msg_api_h.j2')

        target_file_name = component_info['task_name'] + '_msg_api.h'
        target_file_path = self.target_dir + component_info['task_name'] + r'\\' + target_file_name
        with open(target_file_path, 'w') as f:
            h_file = template.render(task_name=component_info['task_name'], events=component_info['event_name'])
            f.write(h_file)

    def generate_stm_c(self, component_info):
        env = Environment(loader=FileSystemLoader(self.template_dir))
        template = env.get_template('templates_stm_c.j2')

        target_file_name = component_info['task_name'] + '_stm.c'
        target_file_path = self.target_dir + component_info['task_name'] + r'\\' + target_file_name
        with open(target_file_path, 'w') as f:
            c_file = template.render(task_name=component_info['task_name'], events=component_info['event_name'], states=component_info['state'])
            f.write(c_file)

    def generate_stm_h(self, component_info):
        env = Environment(loader=FileSystemLoader(self.template_dir))
        template = env.get_template('templates_stm_h.j2')

        target_file_name = component_info['task_name'] + '_stm.h'
        target_file_path = self.target_dir + component_info['task_name'] + r'\\' + target_file_name
        with open(target_file_path, 'w') as f:
            h_file = template.render(task_name=component_info['task_name'], events=component_info['event_name'], states=component_info['state'])
            f.write(h_file)

    def generate_api_h(self, component_info):
        env = Environment(loader=FileSystemLoader(self.template_dir))
        template = env.get_template('templates_api_h.j2')

        target_file_name = component_info['task_name'] + '_api.h'
        target_file_path = self.target_dir + component_info['task_name'] + r'\\' + target_file_name
        with open(target_file_path, 'w') as f:
            h_file = template.render(task_name=component_info['task_name'])
            f.write(h_file)

if __name__ == '__main__':
    instance = LoadConf()
    component_list_in_conf = instance.load_component()
    valid_component_list = instance.check_component_validation(component_list_in_conf)
    instance.generate_store_dir(valid_component_list)
    component_info_dict = instance.parse_component_conf(valid_component_list)

    component_name_list = list(component_info_dict.keys())

    for component_name in component_name_list:
        instance.generate_taskmain_c(component_info_dict[component_name])
        instance.generate_msg_api_c(component_info_dict[component_name])
        instance.generate_msg_api_h(component_info_dict[component_name])
        instance.generate_stm_c(component_info_dict[component_name])
        instance.generate_stm_h(component_info_dict[component_name])
        instance.generate_api_h(component_info_dict[component_name])