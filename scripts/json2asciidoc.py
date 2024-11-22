import os
import json
import argparse


def format_main_headline(file_name):
    """
    Convert file name to a title-style headline for the AsciiDoc.
    Replaces underscores with spaces and capitalizes the first letter.

    Args:
        file_name (str): The base name of the JSON schema file.

    Returns:
        str: The formatted headline.
    """
    file_name = file_name.replace('_', ' ')  # Replace underscores with spaces
    file_name = file_name.replace('-', ' ')  # Replace hyphens with spaces
    return file_name.capitalize()  # Capitalize the first letter


def escape_special_chars(pattern):
    """
    Escape special characters in the pattern string for AsciiDoc compatibility.

    Args:
        pattern (str): The pattern string to be escaped.

    Returns:
        str: The escaped pattern string.
    """
    pattern = pattern.replace("\\", "\\\\")  # Escape backslashes
    return pattern


def generate_asciidoc_array_of_arrays(items, description):
    """
    Generate AsciiDoc content for an array of arrays, listing each item as a column.

    Args:
        items (list): The list of item schemas in the array.
        description (str): The description of the array.

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


def generate_asciidoc_properties(properties, required_fields, level=2):
    """
    Recursively generate AsciiDoc content for a dictionary of properties.

    Args:
        properties (dict): The dictionary of properties from the JSON schema.
        required_fields (list): The list of required fields.
        level (int): The current heading level in the AsciiDoc file.

    Returns:
        str: The generated AsciiDoc content for the properties.
    """
    asciidoc_content = ""
    
    for prop_name, prop_data in properties.items():
        heading_prefix = "=" * level  # Create heading based on level
        asciidoc_content += f"{heading_prefix} {prop_name}\n"
        asciidoc_content += f"{prop_data.get('description', '')}\n"

        # Handle array types and generate description for array of arrays
        if prop_data.get('type') == "array":
            if isinstance(prop_data['items'], dict) and 'items' in prop_data['items']:
                # Generate list for array of arrays
                asciidoc_content += generate_asciidoc_array_of_arrays(prop_data['items']['items'], prop_data['items'].get('description', '')) + "\n"
            elif isinstance(prop_data['items'], list):
                # If it's a list of items, generate columns description directly
                asciidoc_content += generate_asciidoc_array_of_arrays(prop_data['items'], prop_data.get('description', '')) + "\n"
            else:
                # Simple array, include the description of the array
                asciidoc_content += f"\n{prop_data['items'].get('description', '')}\n"
        
        # Add pattern inline and handle escaping of backslashes and curly braces
        if "pattern" in prop_data:
            pattern = escape_special_chars(prop_data['pattern'])
            asciidoc_content += f"\n*Pattern:* `+{pattern}+`\n"
        
        # Add a new line before required status
        if prop_name in required_fields:
            asciidoc_content += "\n*Required:* Yes\n"
        else:
            asciidoc_content += "\n*Required:* No\n"
        
        asciidoc_content += "\n"
        
        # If there are nested properties, recursively generate content for them
        if "properties" in prop_data:
            nested_required_fields = prop_data.get('required', [])
            asciidoc_content += generate_asciidoc_properties(
                prop_data['properties'], nested_required_fields, level + 1
            )

    return asciidoc_content


def generate_asciidoc(field_name, schema, required_fields):
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
    
    # Generate the content for the properties, recursively handling nested properties
    if 'properties' in field_data:
        asciidoc_content += generate_asciidoc_properties(field_data['properties'], required_fields, level=3)
    elif field_data.get('type') == 'array':
        # Handle array fields directly
        if 'items' in field_data and isinstance(field_data['items'], dict) and 'items' in field_data['items']:
            # Array of arrays, generate list of columns
            asciidoc_content += generate_asciidoc_array_of_arrays(field_data['items']['items'], field_data['items'].get('description', '')) + "\n"
        elif isinstance(field_data['items'], list):
            # Array of simple types, generate columns description
            asciidoc_content += generate_asciidoc_array_of_arrays(field_data['items'], field_data.get('description', '')) + "\n"
        else:
            # Handle single item in array
            asciidoc_content += f"\n{field_data['items'].get('description', 'No description')}\n"
    
    return asciidoc_content


def main():
    """
    Main function to handle command-line arguments, process the JSON schema, and generate the AsciiDoc documentation.
    """
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Generate AsciiDoc documentation for a given JSON schema field or the entire schema.")
    parser.add_argument('json_schema_path', type=str, help="Path to the JSON schema file.")
    parser.add_argument('field_name', type=str, nargs='?', default='', help="Name of the field (e.g., metadata) to generate documentation for. Leave empty to generate documentation for the entire schema.")

    # Parse the arguments
    args = parser.parse_args()
    json_schema_path = args.json_schema_path
    field_name = args.field_name

    # Load the JSON schema
    with open(json_schema_path, 'r') as file:
        schema = json.load(file)

    # Generate documentation for the entire schema if field_name is empty
    if not field_name:
        # Generate AsciiDoc for all fields
        print("Generating AsciiDoc for the entire schema...")

        # Generate the main headline from the file name
        base_filename = os.path.basename(json_schema_path).replace('_', '-')
        headline = format_main_headline(os.path.splitext(base_filename)[0])
        asciidoc_content = f"= {headline}\n\n"

        # Process each field in the schema
        for field in schema['properties']:
            required_fields = schema['properties'][field].get('required', [])
            asciidoc_content += generate_asciidoc(field, schema, required_fields)

        # Save the AsciiDoc content to a file
        base_filename = os.path.basename(json_schema_path).replace('_', '-')
        output_filename = f"{os.path.splitext(base_filename)[0]}.adoc"
    else:
        # Check if the field exists in the schema
        if field_name not in schema['properties']:
            print(f"Error: The field '{field_name}' does not exist in the provided schema.")
            return

        # Get the required fields for the selected field
        required_fields = schema['properties'][field_name].get('required', [])

        # Generate the AsciiDoc content for the specific field
        asciidoc_content = generate_asciidoc(field_name, schema, required_fields)

        # Save the AsciiDoc content to a file
        output_filename = f"{field_name}.adoc"

    # Write the output to a file
    with open(output_filename, 'w') as file:
        file.write(asciidoc_content)

    print(f"AsciiDoc generated successfully! Output saved to {output_filename}")


if __name__ == "__main__":
    main()
