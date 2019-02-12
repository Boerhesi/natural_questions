# coding: utf-8

import json
import os
import sys
import numpy as np
import gzip


class Example(object):
    """Example representation."""

    def __init__(self, json_example, mode='train'):
        self.json_example = json_example
        self.mode = mode

        # Whole example info.
        self.url = json_example['document_url']
        self.title = (
            json_example['document_title']
            if hasattr(json_example, 'document_title') else 'Wikipedia')
        self.example_id = str(self.json_example['example_id'])
        self.document_html = self.json_example['document_html'].encode('utf-8')
        self.document_tokens = self.json_example['document_tokens']
        self.question_text = json_example['question_text']

        if self.mode == 'train':
            if len(json_example['annotations']) != 1:
                raise ValueError(
                    'Train set json_examples should have a single annotation.')
            annotation = json_example['annotations'][0]
            self.has_long_answer = annotation['long_answer']['start_byte'] >= 0
            self.has_short_answer = annotation[
                                        'short_answers'] or annotation['yes_no_answer'] != 'NONE'

        elif self.mode == 'dev':
            if len(json_example['annotations']) != 5:
                raise ValueError('Dev set json_examples should have five annotations.')
            self.has_long_answer = sum([
                annotation['long_answer']['start_byte'] >= 0
                for annotation in json_example['annotations']
            ]) >= 2
            self.has_short_answer = sum([
                bool(annotation['short_answers']) or
                annotation['yes_no_answer'] != 'NONE'
                for annotation in json_example['annotations']
            ]) >= 2

        self.long_answers = [
            a['long_answer']
            for a in json_example['annotations']
            if a['long_answer']['start_byte'] >= 0 and self.has_long_answer
        ]
        self.short_answers = [
            a['short_answers']
            for a in json_example['annotations']
            if a['short_answers'] and self.has_short_answer
        ]
        self.yes_no_answers = [
            a['yes_no_answer']
            for a in json_example['annotations']
            if a['yes_no_answer'] != 'NONE' and self.has_short_answer
        ]
