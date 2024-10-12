import xml.etree.ElementTree as ET


def get_input_file():
    input_file = input("Inserisci il nome del file SDF di input (con estensione .sdf): ")
    return input_file

def get_output_file():
    output_file = input("Inserisci il nome del file URDF di output (con estensione .urdf): ")
    return output_file

def parseBaseLink(base_link):
    inertial = base_link.find('inertial')
    if inertial is None:
        raise ValueError("Il tag 'inertial' manca nel base link.")
    
    mass_element = inertial.find('mass')
    if mass_element is None:
        raise ValueError("Il tag 'mass' manca nel base link.")
    
    mass = mass_element.text.strip()
    inertia = inertial.find('inertia')
    if inertia is None:
        raise ValueError("Il tag 'inertia' manca nel base link.")
        
    # Lettura i valori di inerzia
    ixx = inertia.find('ixx').text if inertia.find('ixx') is not None else '0'
    ixy = inertia.find('ixy').text if inertia.find('ixy') is not None else '0'
    ixz = inertia.find('ixz').text if inertia.find('ixz') is not None else '0'
    iyy = inertia.find('iyy').text if inertia.find('iyy') is not None else '0'
    iyz = inertia.find('iyz').text if inertia.find('iyz') is not None else '0'
    izz = inertia.find('izz').text if inertia.find('izz') is not None else '0'
        
    urdf = f'  <link name="base_link">\n'
    urdf += f'    <inertial>\n'
    urdf += f'      <mass value="{mass}"/>\n'
    urdf += f'      <inertia ixx="{ixx}" ixy="{ixy}" ixz="{ixz}" iyy="{iyy}" iyz="{iyz}" izz="{izz}"/>\n'
    urdf += f'    </inertial>\n'


    visuals = base_link.findall('visual')

    for visual in visuals:
        if visual is not None:
          visual_name = visual.attrib.get('name', 'Nome non trovato')
          # Se 'pose' è presente, usa quel valore
          pose = visual.find('pose')
          if pose is not None:
              pose_values = list(map(float, pose.text.strip().split()))
              xyz = f"{pose_values[0]} {pose_values[1]} {pose_values[2]}"
              rpy = f"{pose_values[3]} {pose_values[4]} {pose_values[5]}"
          else:
              rpy = f"0 0 0"  # Fallback se 'pose' non è presente
              xyz = f"0 0 0"

          urdf += f'    <visual name="{visual_name}">\n'
          urdf += f'      <origin rpy="{rpy}" xyz="{xyz}"/>\n'

          mesh = visual.find('geometry/mesh')
          if mesh is not None:
            # Nome del file dalla URI
            uri = mesh.find('uri').text if mesh is not None else 'unknown_mesh'
            filename = uri.split('/')[-1]  # Estrai solo il nome del file
            if filename.endswith('.stl'):
              filename = filename[:-4] + '.dae' #Sostituzione estenzioni .stl in .dae

            scale = mesh.find('scale').text if mesh is not None else '1 1 1'

            urdf += f'      <geometry>\n'
            urdf += f'        <mesh filename="{filename}" scale="{scale}"/>\n'
            urdf += f'      </geometry>\n'

          else:
            size = visual.find('geometry/plane/size')
            size = size.text + " 0.001" #Terza coordinata mock
            urdf += f'      <geometry>\n'
            urdf += f'        <box size="{size}"/>\n'
            urdf += f'      </geometry>\n'
            urdf += f'<cast_shadows>false</cast_shadows>\n'

          urdf += f'    </visual>\n'

              
    urdf += f'  </link>\n'
    return urdf

def parseRotor(rotor):
    pose = rotor.find('pose')
    if pose is None:
        raise ValueError("Il tag 'pose' manca nel rotore.")
    else:
        pose_values = list(map(float, pose.text.strip().split()))
        xyz = f"{pose_values[0]} {pose_values[1]} {pose_values[2]}"
        rpy = f"{pose_values[3]} {pose_values[4]} {pose_values[5]}"
        
    inertial = rotor.find('inertial')
    if inertial is None:
        raise ValueError("Il tag 'inertial' manca nel rotore.")
    
    mass_element = inertial.find('mass')
    if mass_element is None:
        raise ValueError("Il tag 'mass' manca nel rotore.")
    
    mass = mass_element.text.strip()
    inertia = inertial.find('inertia')
    if inertia is None:
        raise ValueError("Il tag 'inertia' manca nel rotore.")
        
    # Lettura i valori di inerzia
    ixx = inertia.find('ixx').text if inertia.find('ixx') is not None else '0'
    ixy = inertia.find('ixy').text if inertia.find('ixy') is not None else '0'
    ixz = inertia.find('ixz').text if inertia.find('ixz') is not None else '0'
    iyy = inertia.find('iyy').text if inertia.find('iyy') is not None else '0'
    iyz = inertia.find('iyz').text if inertia.find('iyz') is not None else '0'
    izz = inertia.find('izz').text if inertia.find('izz') is not None else '0'
    
    
    urdf = f'  <link name="{rotor.attrib["name"]}">\n'
    urdf += f'    <origin rpy="{rpy}" xyz="{xyz}"/>\n'
    urdf += f'    <inertial>\n'
    urdf += f'      <mass value="{mass}"/>\n'
    urdf += f'      <inertia ixx="{ixx}" ixy="{ixy}" ixz="{ixz}" iyy="{iyy}" iyz="{iyz}" izz="{izz}"/>\n'
    urdf += f'    </inertial>\n'


    visuals = rotor.findall('visual')

    for visual in visuals:

        # Se 'pose' è presente, usa quel valore
        pose = visual.find('pose')
        if pose is not None:
            pose_values = list(map(float, pose.text.strip().split()))
            xyz = f"{pose_values[0]} {pose_values[1]} {pose_values[2]}"
            rpy = f"{pose_values[3]} {pose_values[4]} {pose_values[5]}"
        else:
            rpy = f"0 0 0"  # Fallback se 'pose' non è presente
            xyz = f"0 0 0"

        mesh = visual.find('geometry/mesh')
        

        # Nomi del file dalla URI
        uri = mesh.find('uri').text 
        filename = uri.split('/')[-1]  # Estrazione il nome del file
        
        if filename.endswith('.stl'):
          filename = filename[:-4] + '.dae'

        scale = mesh.find('scale').text if mesh is not None else '1 1 1'

        urdf += f'    <visual>\n'
        urdf += f'      <origin rpy="{rpy}" xyz="{xyz}"/>\n'
        urdf += f'      <geometry>\n'
        urdf += f'        <mesh filename="{filename}" scale="{scale}"/>\n'
        urdf += f'      </geometry>\n'
        urdf += f'    </visual>\n'
    
    urdf += f'  </link>\n'
    return urdf

def getPoseFromRotor(jointname, root): #Funzione per recuperare la 'pose'
    result = '<origin xyz="0 0 0"/>\n'
    for rotor in root.findall('.//link'):
        if str(list(jointname)[0]).startswith(str(rotor.attrib['name'])):
            pose = rotor.find('pose')
            if pose is not None:
                pose_values = list(map(float, pose.text.strip().split()))
                xyz = f"{pose_values[0]} {pose_values[1]} {pose_values[2]}"
                result = f'<origin xyz="{xyz}"/>'
    return result

def parseJoint(joint, root):

    parent_link = joint.find('parent')
    child_link = joint.find('child')
    axis = joint.find('axis')

    if parent_link is None or not parent_link.text:
        raise ValueError("Parent link is missing or doesn't have a valid name.")
    
    if child_link is None or not child_link.text:
        raise ValueError("Child link is missing or doesn't have a valid name.")
    
    urdf = f'  <joint name="{joint.attrib["name"]}" type="{joint.attrib["type"]}">\n'
    urdf += f'    <parent link="{parent_link.text.strip()}"/>\n'
    urdf += f'    <child link="{child_link.text.strip()}"/>\n'
    
    # Assi
    if axis is not None:
        xyz = axis.find('xyz')
        if xyz is not None:
            urdf += f'    <axis xyz="{xyz.text.strip()}"/>\n'
        else:
            print(f"Debug: Joint '{joint.attrib['name']}' axis is missing the 'xyz' element.")
    
        # Limiti
        limit = axis.find('limit')
        if limit is not None:
            lower = limit.find('lower')
            upper = limit.find('upper')
            effort = limit.find('effort') if limit.find('effort') is not None else None
            velocity = limit.find('velocity') if limit.find('velocity') is not None else None
            
            limit_attrs = {
                'lower': lower.text.strip() if lower is not None else None,
                'upper': upper.text.strip() if upper is not None else None,
                'effort': effort.text.strip() if effort is not None else '1.0',  # Default
                'velocity': velocity.text.strip() if velocity is not None else '1.0'  # Default
            }
            
            limit_string = ' '.join(f'{key}="{value}"' for key, value in limit_attrs.items() if value is not None)
            urdf += f'    <limit {limit_string}/>\n'
        else:
            print(f"Debug: Joint '{joint.attrib['name']}' has no limit defined.")
    
    # Origine
        origin = getPoseFromRotor({joint.attrib["name"]}, root);
        urdf += f'    {origin}\n'
    
    # Dinamica
    dynamics = axis.find('dynamics')
    if dynamics is not None:
        damping = dynamics.attrib.get("damping", "0.0")  # Default 
        friction = dynamics.attrib.get("friction", "0.0")  # Default 
        urdf += f'    <dynamics damping="{damping}" friction="{friction}"/>\n'
    
    urdf += f'  </joint>\n'
    
    return urdf


def main():
    print("START")
    input_file = get_input_file()
    output_file = get_output_file()

    tree = ET.parse(input_file)
    root = tree.getroot()
    urdf_output = '<?xml version="1.0" ?>\n<robot name="x500_base">\n'
    
    base_link = root.find('.//link[@name="base_link"]')
    if base_link is None:
        raise ValueError("Missing 'base_link' in the input SDF file.")
    urdf_output += parseBaseLink(base_link)

    # Trova tutti i rotori
    for rotor in root.findall('.//link'):
        if rotor.attrib['name'].startswith('rotor_'):
            urdf_output += parseRotor(rotor)

    for joint in root.findall('.//joint'):
        urdf_output += parseJoint(joint, root)

    urdf_output += '</robot>\n'

    with open(output_file, 'w') as f:
        f.write(urdf_output)
    print("File "+output_file+" correttamente scritto")
    
if __name__ == '__main__':
        main()