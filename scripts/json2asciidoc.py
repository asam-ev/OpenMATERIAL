import os
import json
import argparse
from typing import List, Dict


def format_main_headline(file_name: str) -> str:
    """
    Convert a file name to a title-style headline for the AsciiDoc.

    Args:
        file_name (str): The base name of the JSON schema file.

    Returns:
        str: The formatted headline.
    """
    file_name = file_name.replace('_', ' ')  # Replace underscores with spaces
    file_name = file_name.replace('-', ' ')  # Replace hyphens with spaces
    return file_name.capitalize()  # Capitalize the first letter


def escape_special_chars(pattern: str) -> str:
    """
    Escape special characters in the pattern string for AsciiDoc compatibility.

    Args:
        pattern (str): The pattern string to be escaped.

    Returns:
        str: The escaped pattern string.
    """
    return pattern.replace("\\", "\\\\")  # Escape backslashes


def generate_asciidoc_array_of_arrays(items: List[Dict], description: str, required: bool) -> str:
    """
    Generate AsciiDoc content for an array of arrays, listing each item as a column.

    Args:
        items (list[dict]): The list of item schemas in the array.
        description (str): The description of the array.
        required (bool): True if the field is a required property.

    Returns:
        str: The generated AsciiDoc content describing the columns.
    """
    content = ""
    if description:
        content += f"{description}\n"

    content += "\nColumns of the table:\n\n"

    for idx, item in enumerate(items, start=1):
        item_description = item.get('description', 'No description')
        content += f"- Column {idx}: {item_description}\n"

    return content


def generate_asciidoc_properties(properties: Dict, required_fields: List[str], level: int = 2) -> str:
    """
    Recursively generate AsciiDoc content for a dictionary of properties.

    Args:
        properties (dict): The dictionary of properties from the JSON schema.
        required_fields (list): The list of required fields.
        level (int): The current heading level in the AsciiDoc file. Defaults to 2.

    Returns:
        str: The generated AsciiDoc content for the properties.
    """
    asciidoc_content = ""

    for prop_name, prop_data in properties.items():
        heading_prefix = "=" * level  # Create heading based on level
        asciidoc_content += f"{heading_prefix} {prop_name}\n"
        asciidoc_content += f"{prop_data.get('description', '')}\n"

        # Add data type of the property
        if "type" in prop_data:
            property_type = escape_special_chars(prop_data['type'])
            asciidoc_content += f"\n*Type:* `+{property_type}+` +"

        # Add enum options
        if "enum" in prop_data:
            asciidoc_content += f"\n*Enum:* `+{prop_data['enum']}+` +"

        # Add pattern inline and handle escaping of backslashes and curly braces
        if "pattern" in prop_data:
            pattern = escape_special_chars(prop_data['pattern'])
            asciidoc_content += f"\n*Pattern:* `+{pattern}+` +"

        # Add required status
        asciidoc_content += f"\n*Required:* {'Yes' if prop_name in required_fields else 'No'}\n\n"

        # Handle array types and generate description for array of arrays
        if prop_data.get('type') == "array":
            if isinstance(prop_data['items'], dict) and 'items' in prop_data['items']:
                # Generate list for array of arrays
                asciidoc_content += generate_asciidoc_array_of_arrays(
                    prop_data['items']['items'], prop_data['items'].get('description', ''), prop_name in required_fields
                ) + "\n"
            elif isinstance(prop_data['items'], list):
                # If it's a list of items, generate columns description directly
                asciidoc_content += generate_asciidoc_array_of_arrays(
                    prop_data['items'], prop_data.get('description', ''), prop_name in required_fields
                ) + "\n"
            else:
                # Simple array, include the description of the array
                # Add enum options
                if "enum" in prop_data['items']:
                    asciidoc_content += f"\n*Items enum:* `+{prop_data['items'].get('enum', '')}+` +"
                asciidoc_content += f"\n{prop_data['items'].get('description', '')}\n"


        asciidoc_content += "\n"

        # If there are nested properties, recursively generate content for them
        if "properties" in prop_data:
            nested_required_fields = prop_data.get('required', [])
            asciidoc_content += generate_asciidoc_properties(
                prop_data['properties'], nested_required_fields, level + 1
            )

    return asciidoc_content


def generate_asciidoc_main_field(field_name: str, schema: Dict, is_required: bool, required_fields: List[str]) -> str:
    """
    Generate AsciiDoc content for the specified field based on the JSON schema.

    Args:
        field_name (str): The name of the field to generate documentation for.
        schema (dict): The JSON schema dictionary.
        required_fields (list): List of required fields for the specified field.

    Returns:
        str: The generated AsciiDoc content.
    """
    asciidoc_content = f"== {field_name}\n\n"
    field_data = schema['properties'][field_name]
    asciidoc_content += field_data.get("description", "") + "\n\n"

    if "type" in field_data:
        property_type = escape_special_chars(field_data['type'])
        asciidoc_content += f"\n*Type:* `+{property_type}+` +"
    if "pattern" in field_data:
        pattern = escape_special_chars(field_data['pattern'])
        asciidoc_content += f"\n*Pattern:* `+{pattern}+` +"
    asciidoc_content += f"\n*Required:* {'Yes' if is_required else 'No'}\n\n"

    # Generate the content for the properties, recursively handling nested properties
    if 'properties' in field_data:
        asciidoc_content += generate_asciidoc_properties(field_data['properties'], required_fields, level=3)
    elif field_data.get('type') == 'array':
        if 'items' in field_data and isinstance(field_data['items'], dict) and 'items' in field_data['items']:
            asciidoc_content += generate_asciidoc_array_of_arrays(
                field_data['items']['items'], field_data['items'].get('description', ''), field_name in required_fields
            ) + "\n"
        elif isinstance(field_data['items'], list):
            asciidoc_content += generate_asciidoc_array_of_arrays(
                field_data['items'], field_data.get('description', ''), field_name in required_fields
            ) + "\n"
        else:
            asciidoc_content += f"\n{field_data['items'].get('description', 'No description')}\n"

    return asciidoc_content


def generate_asciidoc_file(json_schema_path: str, output_path: str):
    """
    Generate AsciiDoc file for the given JSON schema.

    Args:
        json_schema_path (str): Path to the json schema.
    """
    with open(json_schema_path, 'r') as file:
        schema = json.load(file)

    base_filename = os.path.basename(json_schema_path).replace('_', '-')
    headline = format_main_headline(os.path.splitext(base_filename)[0])
    asciidoc_content = f"= {headline}\n\n"

    for field in schema['properties']:
        is_required = field in schema.get('required', [])
        required_fields = schema['properties'][field].get('required', [])
        asciidoc_content += generate_asciidoc_main_field(field, schema, is_required, required_fields)

    output_filename = f"{os.path.splitext(base_filename)[0]}.adoc"
    output_file = os.path.join(output_path, output_filename)

    with open(output_file, 'w') as file:
        file.write(asciidoc_content)

    print(f"AsciiDoc generated successfully! Output saved to {output_file}")


def main() -> None:
    """
    Handle command-line arguments, process the JSON schema, and generate the AsciiDoc documentation.
    """
    parser = argparse.ArgumentParser(
        description="Generate AsciiDoc documentation for a JSON schema field or the entire schema.")
    parser.add_argument('json_schema_path', type=str, help="Path to the JSON schema file.")
    args = parser.parse_args()

    generate_asciidoc_file(args.json_schema_path, ".")


if __name__ == "__main__":
    main()
