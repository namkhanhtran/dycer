#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Context(object):
    """
    This class contains tuple (text,date) representing 
    for context part in the query
    """
    def __init__(self, text=None, date=None):
        self.text = text
        self.date = date

class Query(object):
    """
    The implementation of query object
    """
    def __init__(self, entity, context):
        self.entity = entity
        self.context = context

class EntityRecommendation(object):
    def __init__(self, embedding_model, relatedness_model, knowledge_graph=None, temporal_graph=None,
                 text_threshold=0.0, date_threshold=0.0, alpha=0.2, method=2, text_method='lm', lucene_vm_init=False):
        self.embedding_model = embedding_model
        self.relatedness_model = relatedness_model
        self.knowledge_graph = knowledge_graph
        self.temporal_graph = temporal_graph
        self.text_threshold = text_threshold
        self.date_threshold = date_threshold
        self.alpha = alpha  
        self.method = method

        self.text_method = text_method
        if self.text_method == 'lm':
            config = dict()
            config['model'] = 'lm'
            config['index_dir'] = 'index'
            config['smoothing_method'] = 'dirichlet'
            self.searcher = Retrieval(config, lucene_vm_init=lucene_vm_init)

    def get_ranked_entities(self, query):
        related_entities = self.score_entities(query=query)
        related_entities = sorted(related_entities.items(), key=lambda x: x[1], reverse=True)
        return related_entities

    def lm_score_text(self, retrieved_entities, query_entity, entity):
        if entity not in self.knowledge_graph[query_entity] or retrieved_entities is None:
            return 0.0
        sim = 0.0
        for (u, v), w in retrieved_entities.get_scores_sorted():
            if (u == query_entity and v == entity) or (u == entity and v == query_entity):
                sim += w

        return sim / len(self.knowledge_graph[query_entity][entity])
