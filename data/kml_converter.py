# KML Converter

This script converts the old KML format to KML 2.2 with ExtendedData support.

## Usage

```bash
python kml_converter.py <input.kml> <output.kml>
```

## Dependencies
- lxml
- xml.etree.ElementTree

  #!/usr/bin/env python3
"""
KML Converter: Converts old Berkeley Buildings KML with custom XML elements to standard KML 2.2 format
Handles <built>, <summary>, <othername>, and <Image> elements by moving them to ExtendedData
"""

import xml.etree.ElementTree as ET
import sys
from pathlib import Path

def convert_kml(input_file, output_file):
    """Convert non-standard KML to KML 2.2 with ExtendedData"""
    
    # Register namespaces
    namespaces = {
        'kml': 'http://www.opengis.net/kml/2.2'
    }
    
    for prefix, uri in namespaces.items():
        ET.register_namespace(prefix, uri)
    
    # Parse the input file
    tree = ET.parse(input_file)
    root = tree.getroot()
    
    # Find all Placemarks
    ns = {'kml': 'http://www.opengis.net/kml/2.2'}
    placemarks = root.findall('.//kml:Placemark', ns)
    
    print(f"Found {len(placemarks)} placemarks to convert...")
    
    for idx, placemark in enumerate(placemarks):
        # Extract custom elements
        built_elem = placemark.find('built')
        summary_elem = placemark.find('summary')
        othername_elem = placemark.find('othername')
        image_elem = placemark.find('Image')
        
        # Create ExtendedData if we have custom elements
        has_custom_data = any([built_elem is not None, summary_elem is not None, 
                               othername_elem is not None, image_elem is not None])
        
        if has_custom_data:
            # Remove old ExtendedData if exists
            old_extended = placemark.find('ExtendedData')
            if old_extended is not None:
                placemark.remove(old_extended)
            
            # Create new ExtendedData
            extended_data = ET.Element('ExtendedData')
            
            # Move custom elements to ExtendedData
            if built_elem is not None:
                data_elem = ET.SubElement(extended_data, 'Data')
                data_elem.set('name', 'built')
                value_elem = ET.SubElement(data_elem, 'value')
                value_elem.text = built_elem.text if built_elem.text else ''
                placemark.remove(built_elem)
            
            if summary_elem is not None:
                data_elem = ET.SubElement(extended_data, 'Data')
                data_elem.set('name', 'summary')
                value_elem = ET.SubElement(data_elem, 'value')
                value_elem.text = summary_elem.text if summary_elem.text else ''
                placemark.remove(summary_elem)
            
            if othername_elem is not None:
                data_elem = ET.SubElement(extended_data, 'Data')
                data_elem.set('name', 'othername')
                value_elem = ET.SubElement(data_elem, 'value')
                value_elem.text = othername_elem.text if othername_elem.text else ''
                placemark.remove(othername_elem)
            
            if image_elem is not None:
                data_elem = ET.SubElement(extended_data, 'Data')
                data_elem.set('name', 'image')
                value_elem = ET.SubElement(data_elem, 'value')
                value_elem.text = image_elem.text if image_elem.text else ''
                placemark.remove(image_elem)
            
            # Insert ExtendedData after description or name
            insert_pos = len(placemark)
            for i, child in enumerate(placemark):
                if child.tag in ['name', 'description', 'Point', 'Polygon']:
                    insert_pos = i + 1
            placemark.insert(insert_pos, extended_data)
        
        # Progress indicator
        if (idx + 1) % 10 == 0:
            print(f"  Processed {idx + 1} placemarks...")
    
    # Write the converted KML
    tree.write(output_file, encoding='UTF-8', xml_declaration=True)
    print(f"Conversion complete! Output saved to: {output_file}")

if __name__ == '__main__':
    input_path = 'buildings.xml'
    output_path = 'buildings_converted.kml'
    
    if len(sys.argv) > 1:
        input_path = sys.argv[1]
    if len(sys.argv) > 2:
        output_path = sys.argv[2]
    
    if not Path(input_path).exists():
        print(f"Error: Input file '{input_path}' not found")
        sys.exit(1)
    
    convert_kml(input_path, output_path)

