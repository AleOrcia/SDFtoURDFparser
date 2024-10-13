from xml.etree import ElementTree
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement


def parsebaselink(base_link: Element):
    inertial = base_link.find("inertial")
    if inertial is None:
        raise ValueError("Il tag 'inertial' manca nel base link.")

    mass_element = inertial.find("mass")
    if mass_element is None:
        raise ValueError("Il tag 'mass' manca nel base link.")

    mass = mass_element.text.strip()
    inertia = inertial.find("inertia")
    if inertia is None:
        raise ValueError("Il tag 'inertia' manca nel base link.")

    # Lettura i valori di inerzia
    ixx = inertia.find("ixx").text if inertia.find("ixx") is not None else "0"
    ixy = inertia.find("ixy").text if inertia.find("ixy") is not None else "0"
    ixz = inertia.find("ixz").text if inertia.find("ixz") is not None else "0"
    iyy = inertia.find("iyy").text if inertia.find("iyy") is not None else "0"
    iyz = inertia.find("iyz").text if inertia.find("iyz") is not None else "0"
    izz = inertia.find("izz").text if inertia.find("izz") is not None else "0"

    linkel = Element("link", {"name": "base_link"})
    iner = SubElement(linkel, "inertial")
    iner.append(Element("mass", {"value": mass}))
    iner.append(
        Element(
            "inertia",
            {"ixx": ixx, "ixy": ixy, "ixz": ixz, "iyy": iyy, "iyz": iyz, "izz": izz},
        )
    )

    visuals = base_link.findall("visual")

    for visual in visuals:
        if visual is not None:
            visual_name = visual.attrib.get("name", "Nome non trovato")
            # Se 'pose' è presente, usa quel valore
            pose = visual.find("pose")
            if pose is not None:
                pose_values = list(map(float, pose.text.strip().split()))
                xyz = f"{pose_values[0]} {pose_values[1]} {pose_values[2]}"
                rpy = f"{pose_values[3]} {pose_values[4]} {pose_values[5]}"
            else:
                rpy = "0 0 0"  # Fallback se 'pose' non è presente
                xyz = "0 0 0"

            vis = SubElement(linkel, "visual", {"name": visual_name})
            vis.append(Element("origin", {"rpy": rpy, "xyz": xyz}))

            mesh = visual.find("geometry/mesh")
            if mesh is not None:
                # Nome del file dalla URI
                uri = mesh.find("uri").text if mesh is not None else "unknown_mesh"
                filename = uri.split("/")[-1]  # Estrai solo il nome del file
                if filename.endswith(".stl"):
                    filename = (
                        filename[:-4] + ".dae"
                    )  # Sostituzione estenzioni .stl in .dae

                scale = mesh.find("scale").text if mesh is not None else "1 1 1"

                geom = SubElement(vis, "geometry")
                geom.append(Element("mesh", {"filename": filename, "scale": scale}))

            else:
                size = visual.find("geometry/plane/size")
                size = size.text + " 0.001"  # Terza coordinata mock

                geom = SubElement(vis, "geometry")
                geom.append(Element("box", {"size": size}))

                cast_shadows = SubElement(vis, "cast_shadows")
                cast_shadows.text = "false"

    return linkel


def parserotor(rotor):
    pose = rotor.find("pose")
    if pose is None:
        raise ValueError("Il tag 'pose' manca nel rotore.")
    else:
        pose_values = list(map(float, pose.text.strip().split()))
        xyz = f"{pose_values[0]} {pose_values[1]} {pose_values[2]}"
        rpy = f"{pose_values[3]} {pose_values[4]} {pose_values[5]}"

    inertial = rotor.find("inertial")
    if inertial is None:
        raise ValueError("Il tag 'inertial' manca nel rotore.")

    mass_element = inertial.find("mass")
    if mass_element is None:
        raise ValueError("Il tag 'mass' manca nel rotore.")

    mass = mass_element.text.strip()
    inertia = inertial.find("inertia")
    if inertia is None:
        raise ValueError("Il tag 'inertia' manca nel rotore.")

    # Lettura i valori di inerzia
    ixx = inertia.find("ixx").text if inertia.find("ixx") is not None else "0"
    ixy = inertia.find("ixy").text if inertia.find("ixy") is not None else "0"
    ixz = inertia.find("ixz").text if inertia.find("ixz") is not None else "0"
    iyy = inertia.find("iyy").text if inertia.find("iyy") is not None else "0"
    iyz = inertia.find("iyz").text if inertia.find("iyz") is not None else "0"
    izz = inertia.find("izz").text if inertia.find("izz") is not None else "0"

    linkel = Element("link", {"name": rotor.attrib["name"]})
    linkel.append(Element("origin", {"rpy": rpy, "xyz": xyz}))
    iner = SubElement(linkel, "inertial")
    iner.append(Element("mass", {"value": mass}))
    iner.append(
        Element(
            "inertia",
            {"ixx": ixx, "ixy": ixy, "ixz": ixz, "iyy": iyy, "iyz": iyz, "izz": izz},
        )
    )

    visuals = rotor.findall("visual")

    for visual in visuals:
        # Se 'pose' è presente, usa quel valore
        pose = visual.find("pose")
        if pose is not None:
            pose_values = list(map(float, pose.text.strip().split()))
            xyz = f"{pose_values[0]} {pose_values[1]} {pose_values[2]}"
            rpy = f"{pose_values[3]} {pose_values[4]} {pose_values[5]}"
        else:
            rpy = "0 0 0"  # Fallback se 'pose' non è presente
            xyz = "0 0 0"

        mesh = visual.find("geometry/mesh")

        # Nomi del file dalla URI
        uri = mesh.find("uri").text
        filename = uri.split("/")[-1]  # Estrazione il nome del file

        if filename.endswith(".stl"):
            filename = filename[:-4] + ".dae"

        scale = mesh.find("scale").text if mesh is not None else "1 1 1"

        vis = SubElement(
            linkel, "visual", {"name": visual.attrib.get("name", "Nome non trovato")}
        )
        vis.append(Element("origin", {"rpy": rpy, "xyz": xyz}))
        geom = SubElement(vis, "geometry")
        geom.append(Element("mesh", {"filename": filename, "scale": scale}))

    return linkel


def getposefromrotor(jointname, root) -> Element:
    "Funzione per recuperare la 'pose'"

    result = None
    for rotor in root.findall(".//link"):
        if not str(list(jointname)[0]).startswith(str(rotor.attrib["name"])):
            continue

        pose = rotor.find("pose")
        if pose is None:
            continue

        pose_values = list(map(float, pose.text.strip().split()))
        xyz = f"{pose_values[0]} {pose_values[1]} {pose_values[2]}"
        result = Element("origin", {"xyz": xyz})

    if result is None:
        logging.warning(f"La 'pose' del rotore {jointname} non è stata trovata.")
        result = Element("origin", {"xyz": "0 0 0"})

    return result


def parsejoint(joint: Element, root: Element):
    parent_link = joint.find("parent")
    child_link = joint.find("child")
    axis = joint.find("axis")

    if parent_link is None or not parent_link.text:
        raise ValueError("Parent link is missing or doesn't have a valid name.")

    if child_link is None or not child_link.text:
        raise ValueError("Child link is missing or doesn't have a valid name.")

    newjoint = Element(
        "joint", {"name": joint.attrib["name"], "type": joint.attrib["type"]}
    )
    newjoint.append(Element("parent", {"link": parent_link.text.strip()}))
    newjoint.append(Element("child", {"link": child_link.text.strip()}))

    # Assi
    if axis is not None:
        xyz = axis.find("xyz")
        if xyz is not None:
            newjoint.append(Element("axis", {"xyz": xyz.text.strip()}))
        else:
            logging.warning(
                f"Joint '{joint.attrib['name']}' axis is missing the 'xyz' element."
            )

        # Limiti
        limit = axis.find("limit")
        if limit is not None:
            lower = limit.find("lower")
            upper = limit.find("upper")
            effort = limit.find("effort") if limit.find("effort") is not None else None
            velocity = (
                limit.find("velocity") if limit.find("velocity") is not None else None
            )

            limit_attrs = {
                "lower": lower.text.strip() if lower is not None else None,
                "upper": upper.text.strip() if upper is not None else None,
                "effort": effort.text.strip()
                if effort is not None
                else "1.0",  # Default
                "velocity": velocity.text.strip()
                if velocity is not None
                else "1.0",  # Default
            }

            newjoint.append(Element("limit", limit_attrs))

        else:
            logging.warning(f"Joint '{joint.attrib['name']}' has no limit defined.")

    # Origine
    origin = getposefromrotor({joint.attrib["name"]}, root)
    newjoint.append(origin)

    # Dinamica
    dynamics = axis.find("dynamics")
    if dynamics is not None:
        damping = dynamics.attrib.get("damping", "0.0")  # Default
        friction = dynamics.attrib.get("friction", "0.0")  # Default
        newjoint.append(Element("dynamics", {"damping": damping, "friction": friction}))

    return newjoint


def convert(root: Element) -> Element:
    logging.debug("Reading input file: %s", input_file)

    model = root.find(".//model")
    if model is None:
        raise ValueError("Missing 'model' in the input SDF file.")

    modelname = model.attrib["name"]
    logging.debug("Model name: %s", modelname)

    robot = Element("robot", {"name": modelname})

    base_link = root.find('.//link[@name="base_link"]')
    if base_link is None:
        raise ValueError("Missing 'base_link' in the input SDF file.")

    converted_base_link = parsebaselink(base_link)
    robot.append(converted_base_link)

    # Trova tutti i rotori
    for rotor in root.findall(".//link"):
        if rotor.attrib["name"].startswith("rotor_"):
            converted_rotor = parserotor(rotor)
            robot.append(converted_rotor)

    for joint in root.findall(".//joint"):
        converted_joint = parsejoint(joint, root)
        robot.append(converted_joint)

    return robot


if __name__ == "__main__":
    import argparse
    import logging

    parser = argparse.ArgumentParser(description="Convert an SDF file to URDF.")
    parser.add_argument("input", type=str, help="Input SDF file to convert")
    parser.add_argument("output", type=str, help="Output URDF file")
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable debug mode"
    )
    args = parser.parse_args()

    input_file = args.input
    output_file = args.output

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG, format="%(levelname)s: %(message)s")
    else:
        logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    logging.debug("Reading input file: %s", input_file)
    tree = ElementTree.parse(input_file)
    root = tree.getroot()

    logging.debug("Converting SDF to URDF...")
    robot = convert(root)

    logging.debug("Writing output file: %s", output_file)
    tree = ElementTree.ElementTree(robot)
    ET.indent(tree)
    tree.write(output_file, encoding="utf-8", xml_declaration=True)

    logging.info("Done. URDF file saved as %s", output_file)
