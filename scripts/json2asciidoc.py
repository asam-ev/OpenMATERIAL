import json
import argparse


def escape_special_chars(pattern):
    """
    Escape special characters in the pattern string for AsciiDoc compatibility.
    
    Args:
        pattern (str): The pattern string to be escaped.
    
    Returns:
        str: The escaped pattern string.
    """
    pattern = pattern.replace("\\", "\\\\")  # Escape backslashes
    pattern = pattern.replace("{", "\\{").replace("}", "\\}")  # Escape curly braces
    return pattern


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
    asciidoc_content = f"= {field_name.capitalize()}\n\n"
    field_data = schema['properties'][field_name]
    asciidoc_content += field_data.get("description", "") + "\n\n"
    
    for prop_name, prop_data in field_data['properties'].items():
        asciidoc_content += f"== {prop_name}\n"
        asciidoc_content += f"{prop_data.get('description', 'No description')}\n"
        
        # Add pattern inline and handle escaping of backslashes and curly braces
        if "pattern" in prop_data:
            pattern = escape_special_chars(prop_data['pattern'])
            asciidoc_content += f"\n*Pattern:* `{pattern}`\n"
        
        # Add a new line before required status
        if prop_name in required_fields:
            asciidoc_content += "\n*Required:* Yes\n"
        else:
            asciidoc_content += "\n*Required:* No\n"
        
        asciidoc_content += "\n"

    return asciidoc_content


def main():
    """
    Main function to handle command-line arguments, process the JSON schema, and generate the AsciiDoc documentation.
    """
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Generate AsciiDoc documentation for a given JSON schema field.")
    parser.add_argument('json_schema_path', type=str, help="Path to the JSON schema file.")
    parser.add_argument('field_name', type=str, help="Name of the field (e.g., metadata) to generate documentation for.")

    # Parse the arguments
    args = parser.parse_args()
    json_schema_path = args.json_schema_path
    field_name = args.field_name

    # Load the JSON schema
    with open(json_schema_path, 'r') as file:
        schema = json.load(file)

    # Check if the field exists in the schema
    if field_name not in schema['properties']:
        print(f"Error: The field '{field_name}' does not exist in the provided schema.")
        return

    # Get the required fields for the selected field
    required_fields = schema['properties'][field_name].get('required', [])

    # Generate the AsciiDoc content
    asciidoc_content = generate_asciidoc(field_name, schema, required_fields)

    # Save the AsciiDoc content to a file
    output_filename = f"{field_name}.adoc"
    with open(output_filename, 'w') as file:
        file.write(asciidoc_content)

    print(f"AsciiDoc generated successfully! Output saved to {output_filename}")


if __name__ == "__main__":
    main()
