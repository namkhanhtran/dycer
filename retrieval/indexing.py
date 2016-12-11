#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

"""
import sys
from tqdm import tqdm
from lucene_tools import Lucene

index_dir = sys.argv[1]
data_file = sys.argv[2]

indexer = Lucene(index_dir=index_dir)
indexer.open_writer()

prefix = "a1b2c3-"
count = 0
with open(data_file, 'r') as infile:
    for line in tqdm(infile):
        tokens = line.strip().split("\t")
        if len(tokens) < 3:
            print tokens[0]
            continue
        comma = tokens[0].find(",")
        source = tokens[0][1:comma].strip()
        target = tokens[0][comma + 1:-1].strip()
        count += 1

        document = []

        id_field = dict()
        id_field['field_name'] = 'id'
        id_field['field_value'] = prefix + str(count)
        id_field['field_type'] = 'id'  # FIELDTYPE_ID = "id" FIELDTYPE_TEXT_TVP = "text_tvp"
        document.append(id_field)
        source_field = dict()
        source_field['field_name'] = 'source'
        source_field['field_value'] = source
        source_field['field_type'] = 'id'  # FIELDTYPE_ID = "id" FIELDTYPE_TEXT_TVP = "text_tvp"
        document.append(source_field)
        target_field = dict()
        target_field['field_name'] = 'target'
        target_field['field_value'] = target
        target_field['field_type'] = 'id'  # FIELDTYPE_ID = "id" FIELDTYPE_TEXT_TVP = "text_tvp"
        document.append(target_field)
        sections = tokens[2].split("::")

        section_text = ""
        for section in sections:
            if section != '#':
                section_text += " " + section
        if len(section_text) > 0:
            section_field_only = dict()
            section_field_only['field_name'] = 'section_only'
            section_field_only['field_value'] = indexer.preprocess(section_text)
            section_field_only['field_type'] = 'text_tvp'
            document.append(section_field_only)
        if len(tokens) < 4:
            continue
        contents = section_text + " " + tokens[3]
        if len(contents) > 0:
            content_field = dict()
            content_field['field_name'] = 'contents'
            content_field['field_value'] = indexer.preprocess(contents)
            content_field['field_type'] = 'text_tvp'
            document.append(content_field)
        if len(tokens[3]) > 0:
            content_only_field = dict()
            content_only_field['field_name'] = 'content_only'
            content_only_field['field_value'] = indexer.preprocess(tokens[3])
            content_only_field['field_type'] = 'text_tvp'
            document.append(content_only_field)
        indexer.add_document(document)

indexer.close_writer()
