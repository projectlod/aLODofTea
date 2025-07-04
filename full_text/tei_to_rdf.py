import rdflib
from rdflib import Graph, Literal, BNode, URIRef, Namespace
from rdflib.namespace import RDF, RDFS, FOAF, DC, XSD, SKOS
from lxml import etree
import re # Import the re module for regular expressions

def tei_to_rdf(xml_file_path, output_rdf_file, format='turtle'):
    """
    Transforms a TEI XML file into an RDF graph and saves it to a file.
    """
    # 1. Initialize RDF Graph
    g = Graph()

    # 2. Define Namespaces
    TEI_NS = "http://www.tei-c.org/ns/1.0"
    MY_DATA = URIRef("http://example.org/bookoftea/")

    # Define SCHEMA, DBO, and GEO using rdflib.Namespace
    SCHEMA = Namespace("http://schema.org/")
    DBO = Namespace("http://dbpedia.org/ontology/")
    GEO = Namespace("http://www.opengis.net/ont/geosparql#")
    LCSH = URIRef("http://id.loc.gov/authorities/subjects/")

    g.bind("tei", TEI_NS)
    g.bind("mydata", MY_DATA)
    g.bind("foaf", FOAF)
    g.bind("dc", DC)
    g.bind("schema", SCHEMA)
    g.bind("skos", SKOS)
    g.bind("dbo", DBO)
    g.bind("geo", GEO)
    g.bind("lcsh", LCSH)

    # 3. Parse XML
    try:
        tree = etree.parse(xml_file_path)
        root = tree.getroot()
    except etree.XMLSyntaxError as e:
        print(f"Error parsing XML: {e}")
        return
    except FileNotFoundError:
        print(f"Error: XML file not found at {xml_file_path}")
        return

    # Use a base URI for the document itself
    doc_uri = MY_DATA + "the-book-of-tea-digital-edition"

    g.add((doc_uri, RDF.type, SCHEMA.Book))
    g.add((doc_uri, RDF.type, DBO.Work))
    g.add((doc_uri, RDF.type, URIRef(TEI_NS + "TEIDocument"))) # Custom TEI type

    # 4. Extract Data and Create Triples

    # Helper function to get text content from TEI element
    def get_tei_text(element, xpath, default=""):
        node = element.find(f'.//{{{TEI_NS}}}{xpath}')
        return node.text.strip() if node is not None and node.text is not None else default

    # --- Header Information ---
    tei_header = root.find(f'{{{TEI_NS}}}teiHeader')
    if tei_header is not None:
        file_desc = tei_header.find(f'{{{TEI_NS}}}fileDesc')
        if file_desc is not None:
            title_stmt = file_desc.find(f'{{{TEI_NS}}}titleStmt')
            if title_stmt is not None:
                # Title
                title = get_tei_text(title_stmt, 'title')
                if title:
                    g.add((doc_uri, DC.title, Literal(title)))

                # Authors (original)
                for author_elem in title_stmt.findall(f'{{{TEI_NS}}}author'):
                    for pers_name_elem in author_elem.findall(f'{{{TEI_NS}}}persName'):
                        author_forename = get_tei_text(pers_name_elem, 'forename')
                        author_surname = get_tei_text(pers_name_elem, 'surname')
                        if author_forename or author_surname:
                            author_uri = MY_DATA + f"author/{author_forename.replace(' ', '-')}-{author_surname.replace(' ', '-')}"
                            g.add((author_uri, RDF.type, FOAF.Person))
                            g.add((doc_uri, DC.creator, author_uri))
                            if author_forename:
                                g.add((author_uri, FOAF.givenName, Literal(author_forename)))
                            if author_surname:
                                g.add((author_uri, FOAF.familyName, Literal(author_surname)))

                            # Alt name
                            alt_name = pers_name_elem.find(f'{{{TEI_NS}}}note')
                            if alt_name is not None and alt_name.text:
                                g.add((author_uri, SKOS.altLabel, Literal(alt_name.text.strip(), lang=alt_name.get(f'{{{TEI_NS}}}lang', ''))))

                # Compiler (respStmt)
                resp_stmt = title_stmt.find(f'{{{TEI_NS}}}respStmt')
                if resp_stmt is not None:
                    compiler_name_elem = resp_stmt.find(f'{{{TEI_NS}}}name/{{{TEI_NS}}}persName')
                    if compiler_name_elem is not None:
                        compiler_forename = get_tei_text(compiler_name_elem, 'forename')
                        compiler_surname = get_tei_text(compiler_name_elem, 'surname')
                        if compiler_forename or compiler_surname:
                            compiler_uri = MY_DATA + f"person/{compiler_forename.replace(' ', '-')}-{compiler_surname.replace(' ', '-')}"
                            g.add((compiler_uri, RDF.type, FOAF.Person))
                            g.add((compiler_uri, FOAF.givenName, Literal(compiler_forename)))
                            g.add((compiler_uri, FOAF.familyName, Literal(compiler_surname)))
                            g.add((doc_uri, DC.contributor, compiler_uri))
                            g.add((compiler_uri, SCHEMA.roleName, Literal("compiler")))

            # Publication Statement
            publication_stmt = file_desc.find(f'{{{TEI_NS}}}publicationStmt')
            if publication_stmt is not None:
                publisher = get_tei_text(publication_stmt, 'publisher')
                pub_place = get_tei_text(publication_stmt, 'pubPlace/placeName')
                pub_date_elem = publication_stmt.find(f'{{{TEI_NS}}}date') # Renamed to avoid clash with pub_date var
                license_uri = publication_stmt.find(f'{{{TEI_NS}}}availability/{{{TEI_NS}}}licence')

                if publisher:
                    g.add((doc_uri, DC.publisher, Literal(publisher)))
                if pub_place:
                    g.add((doc_uri, SCHEMA.location, Literal(pub_place)))
                if pub_date_elem is not None and pub_date_elem.get('when'):
                    date_string = pub_date_elem.get('when')
                    # Dynamically choose datatype based on date format
                    if re.fullmatch(r'\d{4}-\d{2}-\d{2}', date_string): # YYYY-MM-DD
                        g.add((doc_uri, DC.date, Literal(date_string, datatype=XSD.date)))
                    elif re.fullmatch(r'\d{4}', date_string): # YYYY
                        g.add((doc_uri, DC.date, Literal(date_string, datatype=XSD.gYear)))
                    else: # Fallback to plain string for other formats
                        g.add((doc_uri, DC.date, Literal(date_string)))

                if license_uri is not None and license_uri.get('target'):
                    g.add((doc_uri, DC.rights, URIRef(license_uri.get('target'))))
                    g.add((doc_uri, SCHEMA.license, URIRef(license_uri.get('target'))))

            # Source Description (Original 1906 and Digital version)
            source_desc = file_desc.find(f'{{{TEI_NS}}}sourceDesc')
            if source_desc is not None:
                for bibl_elem in source_desc.findall(f'{{{TEI_NS}}}bibl'):
                    bibl_uri = BNode() # Anonymous node for each bibl
                    g.add((doc_uri, DC.source, bibl_uri))
                    g.add((bibl_uri, RDF.type, SCHEMA.CreativeWork))

                    main_title_elem = bibl_elem.find(f'{{{TEI_NS}}}title[@type="main"]')
                    digital_title_elem = bibl_elem.find(f'{{{TEI_NS}}}title[@type="digital"]')
                    original_title_elem = bibl_elem.find(f'{{{TEI_NS}}}title[@type="original"]')

                    if main_title_elem is not None:
                        g.add((bibl_uri, DC.title, Literal(main_title_elem.text.strip())))
                    elif digital_title_elem is not None:
                         g.add((bibl_uri, DC.title, Literal(digital_title_elem.text.strip(), lang=digital_title_elem.get(f'{{{TEI_NS}}}lang', 'en'))))
                    elif original_title_elem is not None:
                        g.add((bibl_uri, DC.title, Literal(original_title_elem.text.strip(), lang=original_title_elem.get(f'{{{TEI_NS}}}lang', ''))))

                    bibl_author_elem = bibl_elem.find(f'{{{TEI_NS}}}author/{{{TEI_NS}}}persName')
                    if bibl_author_elem is not None:
                        bibl_author_forename = get_tei_text(bibl_author_elem, 'forename')
                        bibl_author_surname = get_tei_text(bibl_author_elem, 'surname')
                        if bibl_author_forename or bibl_author_surname:
                            bibl_author_uri = MY_DATA + f"author/{bibl_author_forename.replace(' ', '-')}-{bibl_author_surname.replace(' ', '-')}"
                            g.add((bibl_author_uri, RDF.type, FOAF.Person))
                            g.add((bibl_uri, DC.creator, bibl_author_uri))
                            if bibl_author_forename: g.add((bibl_author_uri, FOAF.givenName, Literal(bibl_author_forename)))
                            if bibl_author_surname: g.add((bibl_author_uri, FOAF.familyName, Literal(bibl_author_surname)))

                    bibl_publisher = get_tei_text(bibl_elem, 'publisher')
                    if bibl_publisher:
                        g.add((bibl_uri, DC.publisher, Literal(bibl_publisher)))

                    bibl_pub_place = get_tei_text(bibl_elem, 'pubPlace')
                    if bibl_pub_place:
                        g.add((bibl_uri, SCHEMA.location, Literal(bibl_pub_place)))

                    bibl_date_elem = bibl_elem.find(f'{{{TEI_NS}}}date') # Renamed
                    if bibl_date_elem is not None and bibl_date_elem.get('when'):
                        date_string = bibl_date_elem.get('when')
                        # Dynamically choose datatype based on date format
                        if re.fullmatch(r'\d{4}-\d{2}-\d{2}', date_string): # YYYY-MM-DD
                            g.add((bibl_uri, DC.date, Literal(date_string, datatype=XSD.date)))
                        elif re.fullmatch(r'\d{4}', date_string): # YYYY
                            g.add((bibl_uri, DC.date, Literal(date_string, datatype=XSD.gYear)))
                        else: # Fallback to plain string
                            g.add((bibl_uri, DC.date, Literal(date_string)))


                    # Digital version ref
                    ref_elem = bibl_elem.find(f'{{{TEI_NS}}}ref')
                    if ref_elem is not None and ref_elem.get('target'):
                        g.add((bibl_uri, SCHEMA.url, URIRef(ref_elem.get('target'))))

        # --- Profile Description (Languages, Persons, Places, Keywords) ---
        profile_desc = tei_header.find(f'{{{TEI_NS}}}profileDesc')
        if profile_desc is not None:
            # Languages
            for lang_elem in profile_desc.findall(f'{{{TEI_NS}}}langUsage/{{{TEI_NS}}}language'):
                lang_ident = lang_elem.get('ident')
                lang_name = lang_elem.text.strip()
                if lang_ident:
                    g.add((doc_uri, DC.language, Literal(lang_ident))) # ISO 639-2/3 code

            # Persons (contributors & mentions)
            partic_desc = profile_desc.find(f'{{{TEI_NS}}}particDesc')
            if partic_desc is not None:
                for list_person_elem in partic_desc.findall(f'{{{TEI_NS}}}listPerson'):
                    for person_elem in list_person_elem.findall(f'{{{TEI_NS}}}person'):
                        person_id = person_elem.get(f'{{{TEI_NS}}}id')
                        pers_name = get_tei_text(person_elem, 'persName')

                        if person_id:
                            person_uri = MY_DATA + f"person/{person_id}"
                        elif pers_name: # Fallback if no xml:id but has a name
                            person_uri = MY_DATA + f"person/{pers_name.replace(' ', '-').replace('(', '').replace(')', '')}"
                        else:
                            continue # Skip if no identifiable info

                        g.add((person_uri, RDF.type, FOAF.Person))
                        if pers_name:
                            g.add((person_uri, FOAF.name, Literal(pers_name)))

                        occupation = get_tei_text(person_elem, 'occupation')
                        if occupation:
                            g.add((person_uri, SCHEMA.occupation, Literal(occupation)))

                        source_url = person_elem.get('source')
                        if source_url:
                            g.add((person_uri, FOAF.homepage, URIRef(source_url)))

                        # Notes for mentioned persons
                        note_elem = person_elem.find(f'{{{TEI_NS}}}note')
                        if note_elem is not None and note_elem.text:
                            g.add((person_uri, SKOS.note, Literal(note_elem.text.strip())))
                            # Try to extract dates from notes
                            date_from_note = note_elem.find(f'{{{TEI_NS}}}date')
                            if date_from_note is not None and date_from_note.get('from') and date_from_note.get('to') and date_from_note.get('type')=='century':
                                g.add((person_uri, SCHEMA.birthDate, Literal(date_from_note.get('from'), datatype=XSD.gYear)))
                                g.add((person_uri, SCHEMA.deathDate, Literal(date_from_note.get('to'), datatype=XSD.gYear)))


            # Places
            setting_desc = profile_desc.find(f'{{{TEI_NS}}}settingDesc')
            if setting_desc is not None:
                for place_elem in setting_desc.findall(f'{{{TEI_NS}}}listPlace/{{{TEI_NS}}}place'):
                    place_id = place_elem.get(f'{{{TEI_NS}}}id')
                    place_name = get_tei_text(place_elem, 'placeName')
                    geonames_idno = place_elem.find(f'{{{TEI_NS}}}idno[@type="geonames"]')

                    if place_id and place_name:
                        place_uri = MY_DATA + f"place/{place_id}"
                        g.add((place_uri, RDF.type, SCHEMA.Place))
                        g.add((place_uri, SCHEMA.name, Literal(place_name)))
                        if geonames_idno is not None and geonames_idno.text:
                            g.add((place_uri, RDFS.seeAlso, URIRef(geonames_idno.text.strip())))
                            g.add((place_uri, GEO.sfContains, URIRef(geonames_idno.text.strip()))) # Simplified link to GeoSPARQL

            # Keywords / TextClass
            text_class = profile_desc.find(f'{{{TEI_NS}}}textClass')
            if text_class is not None:
                lcsh_code = get_tei_text(text_class, 'classCode[@scheme="LCSH"]')
                if lcsh_code:
                    lcsh_uri = LCSH + lcsh_code.replace(' ', '-')
                    g.add((doc_uri, DC.subject, lcsh_uri))
                    g.add((lcsh_uri, RDF.type, SKOS.Concept))
                    g.add((lcsh_uri, SKOS.prefLabel, Literal(lcsh_code)))


                for term_elem in text_class.findall(f'{{{TEI_NS}}}keywords/{{{TEI_NS}}}term'):
                    term_text = term_elem.text.strip()
                    if term_text:
                        term_uri = MY_DATA + f"concept/{term_text.lower().replace(' ', '-')}-keyword"
                        g.add((term_uri, RDF.type, SKOS.Concept))
                        g.add((term_uri, SKOS.prefLabel, Literal(term_text)))
                        g.add((doc_uri, SCHEMA.keywords, Literal(term_text)))
                        g.add((doc_uri, DC.subject, term_uri))


    # --- Text Body Content (simplified for paragraphs, names, places, terms within text) ---
    text_body = root.find(f'{{{TEI_NS}}}text/{{{TEI_NS}}}body')
    if text_body is not None:
        # We can iterate through paragraphs and extract their content,
        # but connecting each paragraph to RDF is more complex as it requires
        # generating unique URIs for each paragraph and managing their order/hierarchy.
        # For a simple representation, we'll extract entities mentioned within them.

        # Example: Extracting entities mentioned directly within the body text
        for pers_name_elem in text_body.findall(f'.//{{{TEI_NS}}}persName'):
            pers_text = pers_name_elem.text.strip()
            if pers_text:
                # Try to link to existing person URIs from the header's listPerson
                # This is a simple heuristic; a robust solution would use xml:id or more sophisticated matching
                person_ref_id = pers_name_elem.get('ref') # This assumes ref points to an xml:id like #FI
                person_uri = None
                if person_ref_id:
                    person_uri = MY_DATA + f"person/{person_ref_id.lstrip('#')}" # Remove # if present
                else: # Fallback for names without ref
                    # More robust would involve lookup in a dictionary of created person URIs
                    person_uri = MY_DATA + f"person/{pers_text.replace(' ', '-')}-mentioned"

                g.add((person_uri, RDF.type, FOAF.Person))
                g.add((person_uri, FOAF.name, Literal(pers_text)))
                g.add((doc_uri, SCHEMA.mentions, person_uri)) # Document mentions this person

        for place_name_elem in text_body.findall(f'.//{{{TEI_NS}}}placeName'):
            place_text = place_name_elem.text.strip()
            place_ref = place_name_elem.get('ref')
            if place_text:
                place_uri = None
                if place_ref:
                    # Assuming ref points to geonames URL or internal xml:id like #china
                    if place_ref.startswith('https://sws.geonames.org/'):
                        place_uri = URIRef(place_ref)
                    else: # Internal xml:id
                        place_uri = MY_DATA + f"place/{place_ref.lstrip('#')}"
                else:
                    place_uri = MY_DATA + f"place/{place_text.replace(' ', '-')}-mentioned"

                g.add((place_uri, RDF.type, SCHEMA.Place))
                g.add((place_uri, SCHEMA.name, Literal(place_text)))
                g.add((doc_uri, SCHEMA.mentions, place_uri))

        for term_elem in text_body.findall(f'.//{{{TEI_NS}}}term'):
            term_text = term_elem.text.strip()
            term_type = term_elem.get('type')
            if term_text:
                term_uri = MY_DATA + f"term/{term_text.lower().replace(' ', '-')}-intext"
                g.add((term_uri, RDF.type, SKOS.Concept))
                g.add((term_uri, SKOS.prefLabel, Literal(term_text)))
                g.add((doc_uri, SCHEMA.about, term_uri)) # Document is about this concept/term
                if term_type:
                    g.add((term_uri, RDF.type, Literal(term_type))) # Add type as a literal property or custom predicate

        # Basic chapter and paragraph structure (can be expanded)
        for chapter_div in text_body.findall(f'{{{TEI_NS}}}div[@type="chapter"]'):
            chapter_id = chapter_div.get('n')
            chapter_uri = MY_DATA + f"chapter/{chapter_id}"
            g.add((doc_uri, SCHEMA.hasPart, chapter_uri))
            g.add((chapter_uri, RDF.type, SCHEMA.Chapter))
            g.add((chapter_uri, DC.identifier, Literal(chapter_id)))

            # FIX for SyntaxError: invalid predicate - Filter in Python
            chapter_head = None
            for head_elem in chapter_div.findall(f'{{{TEI_NS}}}head'):
                if head_elem.get('type') != 'main':
                    chapter_head = head_elem
                    break

            if chapter_head is not None and chapter_head.text:
                g.add((chapter_uri, DC.title, Literal(chapter_head.text.strip())))

            paragraph_counter = 0
            for paragraph_div in chapter_div.findall(f'{{{TEI_NS}}}div[@type="paragraph"]'):
                paragraph_counter += 1
                paragraph_id = paragraph_div.get('n', f"{chapter_id}.{paragraph_counter}")
                paragraph_uri = MY_DATA + f"paragraph/{paragraph_id}"
                g.add((chapter_uri, SCHEMA.hasPart, paragraph_uri))
                g.add((paragraph_uri, RDF.type, SCHEMA.Paragraph))
                g.add((paragraph_uri, DC.identifier, Literal(paragraph_id)))

                p_text_elem = paragraph_div.find(f'{{{TEI_NS}}}p')
                if p_text_elem is not None:
                    # Get all text content including sub-elements
                    paragraph_content = ''.join(p_text_elem.xpath('.//text()')).strip()
                    g.add((paragraph_uri, SCHEMA.text, Literal(paragraph_content)))


    # 5. Serialize RDF Graph
    g.serialize(destination=output_rdf_file, format=format)
    print(f"Transformation complete! RDF saved to {output_rdf_file} in {format} format.")

# --- How to use the function ---
if __name__ == "__main__":
    xml_input_file = 'tei_book_of_tea.xml'
    output_rdf_file_turtle = 'book_of_tea.ttl'
    output_rdf_file_xml = 'book_of_tea.rdf'

    print(f"Transforming {xml_input_file} to RDF (Turtle)...")
    tei_to_rdf(xml_input_file, output_rdf_file_turtle, format='turtle')

    print(f"\nTransforming {xml_input_file} to RDF (RDF/XML)...")
    tei_to_rdf(xml_input_file, output_rdf_file_xml, format='xml')

    print("\nRemember to validate your RDF output with a tool like Protégé or an online RDF validator if needed.")