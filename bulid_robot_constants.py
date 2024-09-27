import xml.etree.ElementTree as ET

def parse_mujoco_xml(file_path):
    # 解析 XML 文件
    tree = ET.parse(file_path)
    root = tree.getroot()

    # 创建一个空的字典，用于存储提取出来的常量
    constants = {
        "name": "ur5e_robotiq",
        "all_joint_names": [],
        "ik_joint_names": [],
        "arm_joint_names": [],
        "actuator_info": {},
        "all_link_names": [],
        "arm_link_names": [],
        "ee_link_names": [],
        "base_joint": None,
        "ee_site_name": None,
        "grasp_actuator": None,
        "weld_body_name": None
    }

    # 提取 joint 名称
    for joint in root.findall(".//joint"):
        joint_name = joint.get("name")
        if joint_name:
            constants["all_joint_names"].append(joint_name)
            if "wrist" in joint_name or "elbow" in joint_name or "shoulder" in joint_name:
                constants["ik_joint_names"].append(joint_name)
                constants["arm_joint_names"].append(joint_name)
            if "base" in joint_name:
                constants["base_joint"] = joint_name
    
    # 提取 actuator 信息
    for actuator in root.findall(".//actuator/motor"):
        joint_name = actuator.get("joint")
        actuator_name = actuator.get("name")
        if joint_name and actuator_name:
            constants["actuator_info"][joint_name] = actuator_name
        if "grasp" in actuator_name:
            constants["grasp_actuator"] = actuator_name

    # 提取 link (body) 名称
    for body in root.findall(".//body"):
        body_name = body.get("name")
        if body_name:
            constants["all_link_names"].append(body_name)
            if "wrist" in body_name or "forearm" in body_name or "shoulder" in body_name:
                constants["arm_link_names"].append(body_name)
            if "robotiq" in body_name:
                constants["weld_body_name"] = body_name

    # 提取末端执行器 (end-effector) 的 site
    for site in root.findall(".//site"):
        site_name = site.get("name")
        if "ee" in site_name:
            constants["ee_site_name"] = site_name

    # 提取 Robotiq 的末端执行器相关部分
    robotiq_links = ["driver", "spring_link", "pad", "follower", "coupler"]
    for body in root.findall(".//body"):
        body_name = body.get("name")
        if body_name and any(link in body_name for link in robotiq_links):
            constants["ee_link_names"].append(body_name)

    return constants

# 使用解析函数
xml_file = "rocobench\\envs\\assets\\kinova_gen3\\gen3.xml"
robot_constants = parse_mujoco_xml(xml_file)
print(robot_constants)
